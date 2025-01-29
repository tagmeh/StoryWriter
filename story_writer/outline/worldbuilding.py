import logging
from pathlib import Path

from openai import Client

from story_writer.config.models import FIRST_PASS_GENERATION_MODEL
from story_writer.config.prompts import GENERAL_SYSTEM_PROMPT, generate_worldbuilding_prompt
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.story_data_model import StoryData, WorldbuildingData
# from story_writer.utils import load_story_data, save_story_data

log = logging.getLogger(__name__)


def generate_worldbuilding(client: Client, story_root: Path):
    # story_data: StoryData = load_story_data(story_path=story_root)
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)

    log.info(f"Generating Characters for story: '{story_data.general.title}'")

    model = FIRST_PASS_GENERATION_MODEL
    instructions = generate_worldbuilding_prompt(story_data=story_data)
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    # Todo: Potentially add a "Have enough characters" validator, if not, rerun validated_stream_llm
    content, elapsed = validated_stream_llm(
        client=client,
        messages=messages,
        model=model,
        validation_model=WorldbuildingData,
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
