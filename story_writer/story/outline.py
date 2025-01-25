from datetime import datetime
from pathlib import Path

import openai
import pydantic
import yaml

from config import prompts
from config.models import FIRST_PASS_GENERATION_MODEL
from story_writer import response_schemas, utils
from story_writer.llm import stream_llm
from story_writer.story_data_model import GeneralData


def generate_general_story_details(client: openai.Client, user_prompt) -> Path | None:
    """
    Uses the LLM to expand and enhance the user_prompt input to create a complete story from end to end.
    Instructs the LLM to respond with a Title, Genre tags, and the Synopsis (Updated user_prompt input)

    :param client: Facilitates LLM connection and communication
    :param user_prompt: User's initial
    :return: Path to the directory containing the generated story data
    """

    model = FIRST_PASS_GENERATION_MODEL
    instructions = prompts.expand_user_input_prompt(user_prompt)
    messages = [
        {
            "role": "system",
            "content": prompts.GENERAL_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": instructions
        }
    ]
    response_format: dict = response_schemas.story_general_schema

    max_retries = 5
    for attempt in range(max_retries):
        content, elapsed, retries = stream_llm(
            client=client, messages=messages, model=model, response_format=response_format
        )

        try:
            # Validate the LLM response data against the GeneralData pydantic model.
            general_story_data = GeneralData(**content)
            break

        except pydantic.ValidationError as err:
            print(f"GeneralData ValidationError: {err}")
            attempt += 1

    else:
        print(f"Failed to get valid general story data in {max_retries} attempts.")
        raise Exception(f"Failed to get valid general story data in {max_retries} attempts. "
                        f"The model '{model}' may not be suitable for this task. "
                        f"Try another model that supports structured outputs.")

    project_root = Path(__file__).parents[2]  # ../StoryWriter/
    story_root = Path(
        f"{project_root}/stories/{general_story_data.title} - {datetime.now().strftime('%Y%m%d%H%M%S')}")
    story_root.mkdir(parents=True, exist_ok=True)

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(general_story_data.model_dump(mode='json'), f, default_flow_style=False, sort_keys=False)

    file_name = f"expand_initial_prompt-{retries}" if retries > 0 else "expand_initial_prompt"
    utils.log_step(story_root=story_root, messages=messages, file_name=file_name, model=FIRST_PASS_GENERATION_MODEL,
                   settings={}, response_format=response_format, duration=elapsed)

    return story_root


if __name__ == '__main__':
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    prompt = """
        Create a story about a cat with superpowers.
        """
    generate_general_story_details(client, prompt)
