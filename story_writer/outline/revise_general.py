import logging
from pathlib import Path

from openai import Client

from story_writer import settings, utils
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import WorldbuildingData, GeneralData
from story_writer.prompts import generate_worldbuilding_prompt


log = logging.getLogger(__name__)


def regenerate_general_story_details(client: Client, story_root: Path):
    """
    Revise the General themes, genres, and synopsis using the story structure based on the original
    general data. The thought is that the og synopsis triggers a story structure, which inherently gives us the story
    stakes which the synopsis probably lacks. So regenerating the synopsis now that we have a start to finish story
    might give us a better synopsis to work with.
    """
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)

    log.info(f"Regenerating general story details: '{story_data.general.title}'")

    model = settings.LLM.model
    # instructions = generate_worldbuilding_prompt(story_data=story_data)
    instructions = f"""Using the story structure data, revise the Themes, Genres, and the synopsis."

Story Details:
Title: {story_data.general.title}
Themes: {", ".join(story_data.general.themes)}
Genre: {", ".join(story_data.general.genres)}
Synopsis: {story_data.general.synopsis}

Story Structure / Outline:\n
{story_data.structure.style}\n
{story_data.structure.list_key_values_str()}
"""

    messages = [
        {"role": "system", "content": settings.BASIC_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    content, elapsed = get_validated_llm_output(
        client=client,
        messages=messages,
        validation_model=GeneralData,
        model_settings=settings.STAGE.GENERAL,
    )

    story_data.general.themes = content.themes
    story_data.general.genres = content.genres
    story_data.general.synopsis = content.synopsis

    story_data.save_to_file(output_dir=story_root)

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="regenerate_general_story_data",
        model=model,
        settings={},
        response_model=GeneralData,
        duration=elapsed,
    )
