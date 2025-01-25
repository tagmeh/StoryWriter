from story_writer.story_data_model import StoryData
from story_writer.story_structures import StoryStructure

GENERAL_SYSTEM_PROMPT = "You are an experienced story author. You fill your story with world building and character" \
                        "defining details to fill out the story."


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


def generate_story_structure_prompt(story_structure: StoryStructure, story_data: StoryData) -> str:
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
    Genres: {', '.join(story_data.general.genres)}
    Themes: {', '.join(story_data.general.themes)}
    Synopsis: {story_data.general.synopsis}
    """
