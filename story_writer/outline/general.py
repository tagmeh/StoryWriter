import logging
from pathlib import Path

import openai

from story_writer import settings
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models.general import GeneralData
from story_writer.prompts import expand_user_input_prompt

log = logging.getLogger(__name__)


def generate_general_story_details(client: openai.Client, user_prompt) -> None:
    """
    Uses the LLM to expand and enhance the user_prompt input to create a complete outline from end to end.
    Instructs the LLM to respond with a Title, Genre tags, and the Synopsis (Updated user_prompt input)

    :param client: Facilitates LLM connection and communication
    :param user_prompt: User's initial input to generate am outline
    :return: Path to the directory containing the generated outline data
    """
    log.info("Generating Initial General Story Details (Title, Genres, Themes, and a Synopsis).")
    instructions = expand_user_input_prompt(user_prompt)
    messages = [
        {"role": "system", "content": settings.basic_system_prompt},
        {"role": "user", "content": instructions},
    ]

    general_story_data, elapsed = get_validated_llm_output(
        client=client,
        messages=messages,
        validation_model=GeneralData,
        model_settings=settings.stage.general,
        log_file_name="expand_initial_prompt",
    )

    settings.story_dir = Path(str(settings.story_dir) + general_story_data.title)
    print(f"{settings.story_dir=}")

    story_data = StoryData(general=general_story_data)  # Initial StoryData creation.

    # TODO: Update save_to_file to use the storyData object story_dir property
    story_data.save_to_file(output_dir=settings.story_dir)

    # log_step(
    #     story_root=story_root,
    #     messages=messages,
    #     file_name="expand_initial_prompt",
    #     model=settings.llm.model,
    #     settings={},
    #     response_model=GeneralData,
    #     duration=elapsed,
    # )
