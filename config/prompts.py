from pprint import pprint

from config.story_settings import SCENES_PER_CHAPTER_MINIMUM_COUNT, CHAPTER_MINIMUM_COUNT
from story_writer.story_data_model import StoryData, ChapterData
from story_writer.story_structures import StoryStructure

GENERAL_SYSTEM_PROMPT = "You are an experienced story author. You fill your story with world building and character defining details to fill out the story."


def expand_user_input_prompt(user_input: str) -> str:
    """
    Returns a prompt to direct the LLM to expand on the user's input.
    The LLM's output is expected to follow a specific json format:
        {
            "title": "Expanded Story",
            "themes": ["Slice of Life", "Romance", "Comedy"],
            "genres": ["Fantasy", "Adventure"],
            "synopsis": "Expanded story based on user input."
        }

    :param user_input: Initial user input to start creating a story.
    :return: A prompt to direct the LLM to expand on the user's input.
    """
    return f"""Expand and elaborate on the user input (below) and work out a complete story from start to finish.
Respond with a clever title, fitting genre tags, the general themes, and the improved and expanded synopsis.
Add details to the story to make it more engaging and interesting.

Who is the protagonist? What are their goals and motivations?
Who or what is the antagonist? What is their goal?
What are the main conflicts in the story?

User Input: {user_input}

Respond with some title options, the genre tags, a general themes, and the synopsis.
"""


def generate_story_structure_prompt(story_structure: StoryStructure, story_data: StoryData) -> str:
    """
    Returns a prompt to direct the LLM to generate a story structure based on the story data provided.

    :param story_structure: The story structure style to use for generating the story structure.
    :param story_data: The story data to use as a basis for generating the story structure.
    :return: A prompt to direct the LLM to generate a story structure.
    """
    return f"""Generate a story structure/outline using the following story structure style: {story_structure.value}.
Expand on each point in the story, adding details where appropriate. Avoid dialogue at this stage.

Consider the protagonist's motivations and desires.
What issues does the protagonist run into, how do they overcome them?
Does anyone help or hinder the protagonist?

User Input:
Title: {story_data.general.title}
Themes: {", ".join(story_data.general.themes)}
Genre: {", ".join(story_data.general.genres)}
Synopsis: {story_data.general.synopsis}
"""


def generate_story_characters_prompt(story_data: StoryData) -> str:
    """

    :param story_data:
    :return:
    """
    instructions = f"""Generate a list of the characters in this story. Define the protagonist, their allies, love interests, friends,
family, enemies, and people who pose as obstacles.

What are the ages of these characters.
Do they have any personality quirks that help define them?
What sort of physical features make them stand out to the reader?

Define as many characters as possible.

Story Details:
Title: {story_data.general.title}
Themes: {", ".join(story_data.general.themes)}
Genre: {", ".join(story_data.general.genres)}
Synopsis: {story_data.general.synopsis}

Story Structure/Outline:\n
"""
    for key, value in story_data.structure.model_dump(mode="python").items():
        if not key.startswith("_"):
            instructions += f" {key}: {value}\n"

    return instructions


def generate_story_chapters_prompt(story_data: StoryData) -> str:
    """

    :param story_data:
    :return:
    """
    instructions = f"""Define {CHAPTER_MINIMUM_COUNT + 1}, or more, chapters.
Use the Title, Genres, Themes, story synopsis, and story structure to generate chapters.

Define the chapter title.
Define which story structure point the chapter covers. 
Define the location the chapter takes place in.
Define which characters feature in each chapter.
What are the statuses of each character (ie, deceased, transformed, asleep, dazed, etc).
Multiple chapters can cover the same story structure parts.
And finally, define the general chapter synopsis.

Story Details:
Title: {story_data.general.title}
Themes: {", ".join(story_data.general.themes)}
Genre: {", ".join(story_data.general.genres)}
Synopsis: {story_data.general.synopsis}

Story Structure/Outline:\n
"""
    for key, value in story_data.structure.model_dump(mode="python").items():
        instructions += f" {key}: {value}\n"

    return instructions


def generate_story_chapter_scene_prompt(story_data: StoryData, chapter: ChapterData) -> str:
    return f"""Define {SCENES_PER_CHAPTER_MINIMUM_COUNT + 1} or more scenes for this chapter. Scenes should expand 
on the chapter synopsis.

Define a short summary of the scene.
Define the characters and their statuses in the scene.
Define the location the scene takes place in.
Define 2-5 story beats for this scene.

Themes: {", ".join(story_data.general.themes)}
Genre: {", ".join(story_data.general.genres)}

Chapter Number: {chapter.number}
Chapter Title: {chapter.title}
Story Structure reference: {chapter.story_structure_point}
Relevant Characters: {", ".join([f"{char.name}: {char.status}" for char in [char for char in chapter.characters]])}
Chapter Location: {chapter.location}
Chapter Synopsis: {chapter.synopsis}
"""
