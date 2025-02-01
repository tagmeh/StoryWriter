import logging
from datetime import datetime
from pathlib import Path

import openai

from story_writer import settings
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models.general import GeneralData
from story_writer.prompts import expand_user_input_prompt
from story_writer.utils import log_step

log = logging.getLogger(__name__)


def generate_general_story_details(client: openai.Client, user_prompt) -> Path | None:
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
        {"role": "system", "content": settings.BASIC_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    general_story_data, elapsed = get_validated_llm_output(
        client=client, messages=messages, validation_model=GeneralData, model_settings=settings.STAGE.GENERAL
    )

    project_root = Path(__file__).parents[2]  # ../StoryWriter/
    story_root = Path(f"{project_root}/stories/{datetime.now().timestamp() * 1000:.0f} - {general_story_data.title}")
    story_root.mkdir(parents=True, exist_ok=True)

    story_data = StoryData(general=general_story_data)  # Initial StoryData creation.

    story_data.save_to_file(output_dir=story_root)

    log_step(
        story_root=story_root,
        messages=messages,
        file_name="expand_initial_prompt",
        model=settings.LLM.model,
        settings={},
        response_model=GeneralData,
        duration=elapsed,
    )

    return story_root
