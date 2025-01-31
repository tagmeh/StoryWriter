import logging
from pathlib import Path

from openai import Client

from story_writer import settings, utils
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import CharacterData
from story_writer.prompts import generate_story_characters_prompt

log = logging.getLogger(__name__)


def generate_characters(client: Client, story_root: Path):

    # story_data: StoryData = load_story_data(story_path=story_root)
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)

    log.info(f"Generating Characters for story: '{story_data.general.title}'")

    model = settings.LLM.model
    instructions = generate_story_characters_prompt(story_data=story_data)
    messages = [
        {"role": "system", "content": settings.BASIC_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    # Todo: Potentially add a "Have enough characters" validator, if not, rerun validated_stream_llm
    content, elapsed = get_validated_llm_output(
        client=client, messages=messages, validation_model=CharacterData, model_settings=settings.STAGE.CHARACTERS
    )

    story_data.characters = content

    # save_story_data(story_root, story_data)
    story_data.save_to_file(output_dir=story_root)

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="generate_characters",
        model=model,
        response_model=CharacterData,
        settings={},
        duration=elapsed,
    )
