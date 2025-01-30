import logging
from pathlib import Path

from openai import Client

from story_writer import settings, utils
from story_writer.config.models import FIRST_PASS_GENERATION_MODEL
from story_writer.config.prompts import generate_worldbuilding_prompt
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import WorldbuildingData

# from story_writer.utils import load_story_data, save_story_data

log = logging.getLogger(__name__)


def generate_worldbuilding(client: Client, story_root: Path):
    # story_data: StoryData = load_story_data(story_path=story_root)
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)

    log.info(f"Generating Characters for story: '{story_data.general.title}'")

    model = FIRST_PASS_GENERATION_MODEL
    instructions = generate_worldbuilding_prompt(story_data=story_data)
    messages = [
        {"role": "system", "content": settings.BASIC_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    # Todo: Potentially add a "character number check (too many or too few)" validator, if not, rerun validated_stream_llm
    content, elapsed = get_validated_llm_output(
        client=client,
        messages=messages,
        model=settings.STAGE.WORLDBUILDING.model,
        temperature=settings.STAGE.WORLDBUILDING.temperature,
        validation_model=WorldbuildingData,
        max_tokens=settings.STAGE.WORLDBUILDING.max_tokens,
    )

    story_data.worldbuilding = content

    # save_story_data(story_root, story_data)
    story_data.save_to_file(output_dir=story_root)

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="generate_worldbuilding",
        model=model,
        settings={},
        response_model=WorldbuildingData,
        duration=elapsed,
    )
