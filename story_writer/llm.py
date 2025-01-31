import json
import logging
import re
import time
from json import JSONDecodeError
from pprint import pprint
from typing import TypeVar

import pydantic
from openai import Client, Stream
from pydantic import BaseModel

from story_writer import settings
from story_writer.models.base import StoryStructure
from story_writer.models.utils import create_json_schema
from story_writer.story_config import StageOverrideSettings

T = TypeVar("T", bound=BaseModel)
SS = TypeVar("SS", bound=StoryStructure)

log = logging.getLogger(__name__)


def remove_directional_single_quotes(inp: str) -> str:
    """Removes left and right single quotes."""
    return re.sub("(\u2018|\u2019)", "'", inp)


def remove_end_of_line_indicators(inp: str) -> str:
    """Removes new line indicators that LLMs sometimes add unnecessarily."""
    return re.sub(r"\\\n +\\", "", inp)


def replace_em_dash_with_regular_dash(inp: str) -> str:
    """Replaces the infamous em dash with a regular god-fearing dash."""
    return re.sub("\u2013", "-", inp)


def get_validated_llm_output(
    client: Client,
    messages: list[dict[str, str]],
    validation_model: type[T],
    model_settings: StageOverrideSettings | None = None
) -> (type[T | SS] | list[type[T]], float):

    # Get the default settings.
    llm_settings: dict = settings.LLM.model_dump(mode='python')
    # Update default settings with stage-specific settings.
    if model_settings:
        llm_settings.update(model_settings.model_dump(mode='python', exclude_unset=True))

    start = time.time()
    attempt = 0
    max_retries = settings.LLM_INVALID_OUTPUT_RETRY_COUNT

    while attempt < max_retries:
        content = call_llm(
            client=client,
            messages=messages,
            response_format=create_json_schema(validation_model),
            llm_settings=llm_settings
        )

        try:
            if isinstance(content, dict):
                log.debug("Validating Dict-style output.")
                valid_model = validation_model(**content)
            elif isinstance(content, list):
                log.debug("Validating List-style output.")
                valid_model = [validation_model(**item) for item in content]
            else:
                log.error(f"LLM Output: '{content}' is not supported.")
                attempt += 1
                continue
            attempt = 0
            break

        except pydantic.ValidationError as err:
            log.error(f"GeneralData ValidationError: {err}")
            attempt += 1

    else:
        log.error(f"Failed to get valid story data in {max_retries} attempts.")
        raise Exception(
            f"Failed to get valid general story data in {max_retries} attempts. "
            f"The model '{llm_settings['model']}' may not be suitable for this task. "
            f"Try another model that supports structured outputs."
        )
    elapsed = time.time() - start
    return valid_model, elapsed


def call_llm(
    client: Client,
    messages: list[dict[str, str]],
    response_format: dict | None,
    llm_settings: dict
):
    """
    Calls the LLM. If stream=True (set using user-accessible via config.yaml), the output is streamed to the terminal.

    :param client: OpenAI Client object. Used to make calls to the LLM.
    :param messages: Array of {"role": "system|user", "content": "to LLM str"}
    :param response_format: Optional[dict] json schema for the LLM to output using. Requires platform/model to support
                            "Structured Output"
    """
    max_retries = settings.LLM_EMPTY_OUTPUT_RETRY_COUNT
    retries = 0

    # Output the message contents for use in testing manually.
    for count, message in enumerate(messages):
        log.debug(f"Message: {count} - Role: {message['role']} - Content: \n{message['content']}")

    log.debug(f"Structured Output Object: \n{json.dumps(response_format)}")

    log.debug(f"Calling LLM with settings: {llm_settings}")
    while retries < max_retries:
        response = client.chat.completions.create(
            messages=messages,
            response_format=response_format,
            stream_options={"include_usage": True},  # Doesn't work for LM Studio?
            **llm_settings
        )

        if isinstance(response, Stream):
            output = ""
            for chunk in response:
                if chunk.choices:  # Last response chunk may not have choices, resulting in an IndexError.
                    print(chunk.choices[0].delta.content or "", end="")
                    output += chunk.choices[0].delta.content or ""
            print("")  # Prevents the next print statement from being on the same line as the last chunk.
            log.debug(f"Output Length: {len(output)}")
            log.debug("Usage: Unavailable when streaming output.")
        else:
            output = response.choices[0].message.content
            log.debug(f"Output Length: {len(output)}")
            log.debug(
                f"Usage: Prompt Tokens: {response.usage.prompt_tokens} - "
                f"Completion Tokens: {response.usage.completion_tokens} - "
                f"Total Tokens: {response.usage.total_tokens}"
            )

        log.debug("Processing LLM string output. Removing non-utf-8 characters and other LLM oddities.")
        output = remove_directional_single_quotes(output)
        output = remove_end_of_line_indicators(output)
        output = replace_em_dash_with_regular_dash(output)
        output = output.strip()  # Reduces output that's all spaces and tabs into an empty string for validation.

        if response_format:  # Expectation is that the output will always be an object. Per structured output specs.
            log.debug("LLM called with a response schema, output will be ran through a json serializer.")
            try:
                content = json.loads(output)
                log.debug("Serialized LLM output successfully")
            except JSONDecodeError as err:
                log.error(f'JSONDecodeError: "{err}". Attempts: {retries}, Retrying...')
                retries += 1
                continue

        else:  # Output is a string because there was no structured output/response format.
            log.debug("LLM called without a response schema, output is raw.")
            # Todo: Check to see if the openai package will return an integer if the LLM output is "1" or similar.
            content = output  # Without a response_format, output is expected to just be a string.

        if content == {} or content == [] or content == "":
            log.error(f'No content returned from LLM. "{content}". Attempts: {retries}, Retrying...')
            retries += 1

        else:
            return content

    else:
        log.error(f"Failed to get any data from the LLM in {retries} attempts.")


# def call_llm(client, messages, model, response_format):
#     start = time.time()
#     max_retries = 5
#     retries = 0
#     while retries < max_retries:
#         response = client.chat.completions.create(
#             messages=messages,
#             model=model,
#             response_format=response_format
#         )
#         elapsed = time.time() - start
#
#         try:
#             content = json.loads(response.choices[0].message.content)
#             from pprint import pprint
#             pprint(content, sort_dicts=False)
#         except JSONDecodeError as err:
#             print(f'JSON Error: "{err}" Retrying...')
#             retries += 1
#             continue
#
#         if content == {}:
#             print(f'No content returned from LLM. "{content}')
#             retries += 1
#
#         else:
#             return content, elapsed, retries
#
#     if retries >= max_retries:
#         print(f'Failed to get any data from the LLM in {retries} attempts.')
