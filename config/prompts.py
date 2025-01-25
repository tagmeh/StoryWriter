from story_writer.story_data_model import StoryData

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
    Expand on the user input (below) and work out a complete story from start to finish.
    Respond with a clever title, fitting genre tags, the general themes, and the improved 
    and expanded synopsis.
    
    User Input: {user_input}
    
    Respond with some title options, the genre tags, a general themes, and the synopsis.
    """
