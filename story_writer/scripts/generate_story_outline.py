from openai import Client

from story_writer import settings
from story_writer.outline.chapters import generate_chapters
from story_writer.outline.characters import generate_characters
from story_writer.outline.general import generate_general_story_details
from story_writer.outline.scenes import generate_scenes_for_chapter
from story_writer.outline.structure import generate_story_structure
from story_writer.outline.worldbuilding import generate_worldbuilding


def generate_story_outline(client: Client, prompt: str) -> None:
    """
    Define the steps and call the relevant functions to output a full story outline.

    A full story outline has:
    Title
    Genres
    Themes
    General Synopsis

    Story Structure (Classic, 7 Pinch Point, Dan Harmon's Story Circle, etc.)
        Style
        Structure
            Various properties based on Style (Different properties for different story structures)

    Characters
        Name
        Age
        Role
        Personality

    World Building
        Geography
        Culture
        History
        Politics
        Economy
        Magic_technology
        Religion
        Additional_details

    Chapters
        Title
        Number
        Story Structure Point (what part of the story structure does this chapter take place in)
        Location
        Characters
            Name
            Status
        Synopsis

    Scenes (Per Chapter)
        Number
        Summary
        Characters
            Name
            Status
        Location
        Story Beats (What happens in the scene, should generally follow the chapter's synopsis)

    :return: Each section saves it's data in a StoryData object, which is "cached"
             as a file in /stories/<story title>/story_data.(json|yaml)
    """

    # Generates the Title, Genres, Themes, and a Synopsis.
    story_root = generate_general_story_details(client, prompt.strip())

    # Uses the user-setting STORY_STRUCTURE_STYLE and story general data (above) to fill out the given story structure.
    generate_story_structure(client, story_root, story_structure=settings.STORY_STRUCTURE_STYLE)

    generate_worldbuilding(client, story_root)

    generate_characters(client, story_root)

    generate_chapters(client, story_root)

    generate_scenes_for_chapter(client, story_root)
