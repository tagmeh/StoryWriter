import logging

from openai import Client

from story_writer import settings
from story_writer.constants import StoryStructureEnum
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.prompts import generate_story_structure_prompt
from story_writer.utils import get_story_structure_model

log = logging.getLogger(__name__)


def generate_story_structure(
    client: Client,
    story_structure: StoryStructureEnum = StoryStructureEnum.CLASSIC_STORY_STRUCTURE,
):
    """
    Uses the LLM to generate the story structure based on the user's selected story structure.

    :param client: Facilitates LLM connection and communication
    :param story_structure: Enum representing the selected story structure

    :return: None (Saves parameters used in the LLM call in the story directory /logs/,
             updates the story_data.yaml with the structured return data.)
    """
    story_data: StoryData = StoryData.load_from_file(saved_dir=settings.story_dir)

    if not story_data.general:
        raise Exception("General story details do not exist, create a new story before generating the story structure.")

    story_structure_model = get_story_structure_model(story_structure)
    instructions = generate_story_structure_prompt(story_structure, story_data)
    messages = [
        {"role": "system", "content": settings.basic_system_prompt},
        {"role": "user", "content": instructions},
    ]

    # Call to the LLM, should be able to trust the returned pydantic model.
    story_structure_data, elapsed = get_validated_llm_output(
        client=client,
        messages=messages,
        validation_model=story_structure_model,
        model_settings=settings.stage.structure,
        log_file_name="generate_story_structure",
    )

    story_data.structure = story_structure_data

    story_data.save_to_file(output_dir=settings.story_dir)

    # utils.log_step(
    #     story_root=story_root,
    #     messages=messages,
    #     file_name="generate_story_structure",
    #     model=model,
    #     settings={},
    #     response_model=story_structure_model,
    #     duration=elapsed,
    # )
