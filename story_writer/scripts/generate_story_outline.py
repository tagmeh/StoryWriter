from openai import Client

from story_writer import settings
from story_writer.outline import (
    generate_chapters,
    generate_characters,
    generate_general_story_details,
    regenerate_general_story_details,
    generate_scenes_for_chapter,
    generate_story_structure,
    generate_worldbuilding,
)


def generate_story_outline(client: Client, prompt: str) -> None:
    """
    Define the steps and call the relevant functions to output a full story outline.

    :return: Each section saves its data in a StoryData object, which is "cached"
             as a file in /stories/<story title>/story_data.(json|yaml)
    """

    # Generates the Title, Genres, Themes, and a Synopsis.
    story_root = generate_general_story_details(client, prompt.strip())

    # Uses the user-setting STORY_STRUCTURE_STYLE and story general data (above) to fill out the given story structure.
    generate_story_structure(client, story_root, story_structure=settings.STORY_STRUCTURE_STYLE)

    # Redo the General Story data after getting the story structure.
    regenerate_general_story_details(client, story_root)

    generate_worldbuilding(client, story_root)

    generate_characters(client, story_root)

    generate_chapters(client, story_root)

    generate_scenes_for_chapter(client, story_root)
