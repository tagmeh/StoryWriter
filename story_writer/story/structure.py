from pathlib import Path

import yaml
from openai import Client

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_structure_prompt
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.response_schemas import story_structure_schema
from story_writer.story_data_model import StoryData, StoryStructureData
from story_writer.story_structures import (
    StoryStructure,
    get_story_structure_schema,
    get_story_structure_model,
)


def generate_story_structure(
    client: Client,
    story_root: Path,
    story_structure: StoryStructure = StoryStructure.CLASSIC,
):
    """
    Uses the LLM to generate the story structure based on the user's selected story structure.

    :param client: Facilitates LLM connection and communication
    :param story_root: Path to the directory containing the generated story data
    :param story_structure: Enum representing the selected story structure

    :return: None (Saves parameters used in the LLM call in the story directory /logs/,
             updates the story_data.yaml with the structured return data.)
    """
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = StoryData(**yaml.safe_load(f))

    if not story_data.general:
        raise Exception(
            "General story details do not exist, create a new story before generating the story structure."
        )

    model = FIRST_PASS_GENERATION_MODEL
    instructions = generate_story_structure_prompt(story_structure, story_data)
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]
    response_format: dict = story_structure_schema
    response_format["json_schema"]["schema"] = get_story_structure_schema(
        story_structure
    )

    # Get the pydantic model used to validate the LLM's output.
    story_structure_model = get_story_structure_model(story_structure)

    # Call to the LLM, should be able to trust the returned pydantic model.
    story_structure_data, elapsed = validated_stream_llm(
        client=client,
        messages=messages,
        model=model,
        response_format=response_format,
        validation_model=story_structure_model,
    )

    story_structure_data = StoryStructureData(
        style=story_structure.value, structure=story_structure_data
    )

    story_data.structure = story_structure_data

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(
            story_data.model_dump(mode="json"),
            f,
            default_flow_style=False,
            sort_keys=False,
        )

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="generate_story_structure",
        model=model,
        settings={},
        response_format=response_format,
        duration=elapsed,
    )
