from pathlib import Path
from typing import Type

from openai import Client

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_structure_prompt
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.story_data_model import StoryData
from story_writer.story_structures import StoryStructureEnum, BaseModel
from story_writer.utils import load_story_data, save_story_data


def generate_story_structure(
    client: Client,
    story_root: Path,
    story_structure: Type[BaseModel] = StoryStructureEnum.CLASSIC,
):
    """
    Uses the LLM to generate the story structure based on the user's selected story structure.

    :param client: Facilitates LLM connection and communication
    :param story_root: Path to the directory containing the generated story data
    :param story_structure: Enum representing the selected story structure

    :return: None (Saves parameters used in the LLM call in the story directory /logs/,
             updates the story_data.yaml with the structured return data.)
    """
    story_data: StoryData = load_story_data(story_path=story_root)

    if not story_data.general:
        raise Exception("General story details do not exist, create a new story before generating the story structure.")

    model = FIRST_PASS_GENERATION_MODEL
    print(f"{story_structure=}")
    print(f"{story_structure.value=}")
    instructions = generate_story_structure_prompt(story_structure.value, story_data)
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    # Call to the LLM, should be able to trust the returned pydantic model.
    story_structure_data, elapsed = validated_stream_llm(
        client=client,
        messages=messages,
        model=model,
        validation_model=story_structure.value,
    )

    story_data.structure = story_structure.value(**story_structure_data)

    save_story_data(story_root, story_data)

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="generate_story_structure",
        model=model,
        settings={},
        response_model=story_structure.value,
        duration=elapsed,
    )
