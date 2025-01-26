from pathlib import Path

import yaml
from openai import Client

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_characters_prompt
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.response_schemas import story_characters_schema
from story_writer.story_data_model import StoryData, CharacterData


def generate_characters(client: Client, story_root: Path):
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = StoryData(**yaml.safe_load(f))

    model = FIRST_PASS_GENERATION_MODEL
    instructions = generate_story_characters_prompt(story_data=story_data)
    messages = [
        {
            "role": "system",
            "content": GENERAL_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": instructions
        }
    ]
    response_format: dict = story_characters_schema

    # Todo: Potentially add a "Have enough characters" validator, if not, rerun validated_stream_llm
    content, elapsed = validated_stream_llm(
        client=client, messages=messages, model=model, response_format=response_format, validation_model=CharacterData
    )

    story_data.characters = content

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data.model_dump(mode='json'), f, default_flow_style=False, sort_keys=False)

    utils.log_step(story_root=story_root, messages=messages, file_name="generate_characters",
                   model=model, settings={}, response_format=response_format, duration=elapsed)
