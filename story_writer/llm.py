import json
import time
from json import JSONDecodeError


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

        elapsed = time.time() - start

        try:
            content = json.loads(output)
            from pprint import pprint
            pprint(content, sort_dicts=False)
        except JSONDecodeError as err:
            print(f'JSON Error: "{err}" Retrying...')
            retries += 1
            continue

        if content == {}:
            print(f'No content returned from LLM. "{content}')
            retries += 1

        else:
            return content, elapsed, retries

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
