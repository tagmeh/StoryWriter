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
    return f"""
    Expand and elaborate on the user input (below) and work out a complete story from start to finish.
    Respond with a clever title, fitting genre tags, the general themes, and the improved and expanded synopsis.
    Add details to the story to make it more engaging and interesting.
    
    Who is the protagonist? What are their goals and motivations?
    Who or what is the antagonist? What is their goal?
    What are the main conflicts in the story?
    
    User Input: {user_input}
    
    Respond with some title options, the genre tags, a general themes, and the synopsis.
    """


def generate_story_structure_prompt(
    story_structure: StoryStructure, story_data: StoryData
) -> str:
    """
    Returns a prompt to direct the LLM to generate a story structure based on the story data provided.

    :param story_structure: The story structure style to use for generating the story structure.
    :param story_data: The story data to use as a basis for generating the story structure.
    :return: A prompt to direct the LLM to generate a story structure.
    """
    return f"""
    Generate a story structure/outline using the following story structure style: {story_structure.value}.
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
    instructions = f"""
    Generate a list of the characters in this story. Define the protagonist, their allies, love interests, friends,
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

    Story Structure:
    """
    for key, value in story_data.structure.model_dump(mode="python").items():
        if not key.startswith("_"):
            instructions += f" {key}: {value}"

    return instructions


def generate_story_chapters_prompt(story_data: StoryData) -> str:
    """

    :param story_data:
    :return:
    """
    instructions = f"""
    Generate between 5 and 10 high-level chapters. Chapters will be broken up into scenes in the future, so these 
    chapters should be considered more higher level or more generic. Use the Title, Genres, Themes,
    general story synopsis, and story structure/outline to generate a number 
    of chapters. Chapters should span from the beginning to the end of the story. 

    Define the location the chapter takes place in.
    Define which characters feature in each chapter.
    What are the statuses of each character (ie, deceased, transformed, asleep, dazed, etc).
    Define which story structure point the chapter covers. 
    Multiple chapters can cover the same story structure parts.

    Story Details:
    Title: {story_data.general.title}
    Themes: {", ".join(story_data.general.themes)}
    Genre: {", ".join(story_data.general.genres)}
    Synopsis: {story_data.general.synopsis}

    Story Structure/Outline:
    Structure:
    """
    for key, value in story_data.structure.model_dump(mode="python").items():
        instructions += f" {key}: {value}"

    return instructions


def generate_story_chapter_scene_prompt(
    story_data: StoryData, chapter: ChapterData
) -> str:
    return f"""
    Generate at least 5 expanded scenes, in order, for this chapter. Go into more detail, describing
    the story in more detail, encapsulated within the scene. Output the location the scene takes
    place in, the characters in the scene, and the story beats detailing the events happening.
    Avoid dialogue, if a character speaks, detail what they say without quotes. IE. Jeff greeted his friends.

    Themes: {", ".join(story_data.general.themes)}
    Genre: {", ".join(story_data.general.genres)}
    Synopsis: {story_data.general.synopsis}

    Chapter Number: {chapter.chapter_number}
    Chapter Title: {chapter.title}
    Chapter Story Structure reference: {chapter.story_structure_point}
    Characters: {", ".join([f"{char.name}: {char.status}" for char in [char for char in chapter.characters]])}
    Locations: {chapter.location}
    Synopsis: {chapter.synopsis}
    """
