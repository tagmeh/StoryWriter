import json
import time
from json import JSONDecodeError
from typing import TypeVar, Type

import pydantic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def validated_stream_llm(client, messages, model, response_format, validation_model: Type[T], max_retries: int = 5) -> (Type[T], float):
    max_retries = max_retries
    for attempt in range(max_retries):
        content, elapsed = stream_llm(
            client=client, messages=messages, model=model, response_format=response_format
        )

        try:
            # Validate the LLM response data against the pydantic model.
            valid_model = validation_model(**content)
            break

        except pydantic.ValidationError as err:
            print(f"GeneralData ValidationError: {err}")
            attempt += 1

    else:
        print(f"Failed to get valid general story data in {max_retries} attempts.")
        raise Exception(f"Failed to get valid general story data in {max_retries} attempts. "
                        f"The model '{model}' may not be suitable for this task. "
                        f"Try another model that supports structured outputs.")

    return valid_model, elapsed


def stream_llm(client, messages, model, response_format):
    start = time.time()
    max_retries = 5
    retries = 0
    while retries < max_retries:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            response_format=response_format,
            stream=True,
            stream_options={"include_usage": True}  # Doesn't work for LM Studio?
        )

        output = ""
        for chunk in response:
            if chunk.choices:  # Last response chunk may not have choices, resulting in an IndexError.
                print(chunk.choices[0].delta.content or "", end="")
                output += chunk.choices[0].delta.content or ""
        print("")  # Prevents the next print statement from being on the same line as the last chunk.

        elapsed = time.time() - start

        try:
            content = json.loads(output)
        except JSONDecodeError as err:
            print(f'JSON Error: "{err}" Retrying...')
            retries += 1
            continue

        if content == {}:
            print(f'No content returned from LLM. "{content}')
            retries += 1

        else:
            return content, elapsed

    if retries >= max_retries:
        print(f'Failed to get any data from the LLM in {retries} attempts.')


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
