from datetime import datetime
from pathlib import Path

from openai import Client

from story_writer import settings
from story_writer.outline import (
    generate_chapters,
    generate_characters,
    generate_general_story_details,
    generate_scenes_for_chapter,
    generate_story_structure,
    generate_worldbuilding,
    regenerate_general_story_details,
)


def generate_story_outline(client: Client, prompt: str) -> None:
    """
    Define the steps and call the relevant functions to output a full story outline.

    :return: Each section saves its data in a StoryData object, which is "cached"
             as a file in /stories/<story title>/story_data.(json|yaml)
    """

    stories_dir = Path(__file__).parents[2]

    settings.story_dir = stories_dir / "stories" / f"{datetime.now().timestamp() * 1000:.0f} - "

    # Generates the Title, Genres, Themes, and a Synopsis.
    generate_general_story_details(client, prompt.strip())

    # Uses the user-setting STORY_STRUCTURE_STYLE and story general data (above) to fill out the given story structure.
    generate_story_structure(client, story_structure=settings.story_structure_style)

    # Redo the General Story data after getting the story structure.
    regenerate_general_story_details(client)

    generate_worldbuilding(client)

    generate_characters(client)

    generate_chapters(client)

    generate_scenes_for_chapter(client)
