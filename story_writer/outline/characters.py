import logging
from pathlib import Path

from openai import Client

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_characters_prompt
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.response_schemas import story_characters_schema
from story_writer.story_data_model import CharacterData, StoryData
from story_writer.utils import load_story_data, save_story_data

log = logging.getLogger(__name__)


def generate_characters(client: Client, story_root: Path):

    story_data: StoryData = load_story_data(story_path=story_root)

    log.info(f"Generating Characters for story: '{story_data.general.title}'")

    model = FIRST_PASS_GENERATION_MODEL
    instructions = generate_story_characters_prompt(story_data=story_data)
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]
    response_format: dict = story_characters_schema

    # Todo: Potentially add a "Have enough characters" validator, if not, rerun validated_stream_llm
    content, elapsed = validated_stream_llm(
        client=client,
        messages=messages,
        model=model,
        response_format=response_format,
        validation_model=CharacterData,
    )

    story_data.characters = content

    save_story_data(story_root, story_data)

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="generate_characters",
        model=model,
        settings={},
        response_format=response_format,
        duration=elapsed,
    )
