import json
import logging
import re
import time
from json import JSONDecodeError
from typing import TypeVar

import pydantic
from pydantic import BaseModel

from config.story_settings import (
    LLM_EMPTY_OUTPUT_RETRY_COUNT,
    LLM_INVALID_OUTPUT_RETRY_COUNT,
)

T = TypeVar("T", bound=BaseModel)

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


def validated_stream_llm(
    client,
    messages,
    model,
    validation_model: type[T],
    response_format: dict | None = None,
    max_retries: int = LLM_INVALID_OUTPUT_RETRY_COUNT,
) -> (type[T] | list[type[T]], float):
    start = time.time()
    max_retries = max_retries
    attempt = 0
    while attempt < max_retries:
        content = stream_llm(
            client=client,
            messages=messages,
            model=model,
            response_format=response_format,
        )

        try:
            if isinstance(content, dict):
                valid_model = validation_model(**content)
            elif isinstance(content, list):
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
        log.error(f"Failed to get valid general story data in {max_retries} attempts.")
        raise Exception(
            f"Failed to get valid general story data in {max_retries} attempts. "
            f"The model '{model}' may not be suitable for this task. "
            f"Try another model that supports structured outputs."
        )
    elapsed = time.time() - start
    return valid_model, elapsed


def stream_llm(
    client,
    messages,
    model,
    response_format: str | None,
    max_retries: int = LLM_EMPTY_OUTPUT_RETRY_COUNT,
):
    max_retries = max_retries
    retries = 0
    while retries < max_retries:
        for count, message in enumerate(messages):
            log.debug(f"Role: {message['role']} - Message: \n{message['content']}")

        response = client.chat.completions.create(
            messages=messages,
            model=model,
            response_format=response_format,
            stream=True,
            stream_options={"include_usage": True},  # Doesn't work for LM Studio?
            temperature=0.85,
        )

        output = ""
        for chunk in response:
            if chunk.choices:  # Last response chunk may not have choices, resulting in an IndexError.
                print(chunk.choices[0].delta.content or "", end="")
                output += chunk.choices[0].delta.content or ""
        print("")  # Prevents the next print statement from being on the same line as the last chunk.

        # String cleanup, pre-json.loads()
        output = remove_directional_single_quotes(output)
        output = remove_end_of_line_indicators(output)
        output = replace_em_dash_with_regular_dash(output)
        output = output.strip()  # Reduces output that's all spaces and tabs into an empty string for validation.

        if response_format:  # Expectation is that the output will always be an object. Per structured output specs.
            log.debug("LLM called with a response schema, output will be ran through a json serializer.")
            try:
                content = json.loads(output)
            except JSONDecodeError as err:
                log.error(f'JSONDecodeError: "{err}" Retrying...')
                retries += 1
                continue

        else:
            log.debug("LLM called without a response schema, output is raw.")
            # Todo: Check to see if the openai package will return an integer if the LLM output is "1" or similar.
            content = output  # Without a response_format, output is expected to just be a string.

        if content == {} or content == [] or content == "":
            log.error(f'No content returned from LLM. "{content}", Retrying...')
            retries += 1

        else:
            return content

    # if retries >= max_retries:
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
