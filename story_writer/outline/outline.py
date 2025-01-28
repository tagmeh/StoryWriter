import logging
from datetime import datetime
from pathlib import Path

import openai

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, expand_user_input_prompt
from story_writer.llm import validated_stream_llm
from story_writer.story_data_model import GeneralData, StoryData
from story_writer.utils import log_step, save_story_data

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
    model = FIRST_PASS_GENERATION_MODEL
    instructions = expand_user_input_prompt(user_prompt)
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {"role": "user", "content": instructions},
    ]

    general_story_data, elapsed = validated_stream_llm(
        client=client,
        messages=messages,
        model=model,
        validation_model=GeneralData,
    )

    project_root = Path(__file__).parents[2]  # ../StoryWriter/
    story_root = Path(f"{project_root}/stories/{general_story_data.title} - {datetime.now().timestamp() * 1000:.0f}")
    story_root.mkdir(parents=True, exist_ok=True)

    story_data = StoryData(general=general_story_data)  # Initial StoryData creation.

    save_story_data(story_root, story_data)

    log_step(
        story_root=story_root,
        messages=messages,
        file_name="expand_initial_prompt",
        model=FIRST_PASS_GENERATION_MODEL,
        settings={},
        response_model=GeneralData,
        duration=elapsed,
    )

    return story_root


if __name__ == "__main__":
    from openai import OpenAI

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    prompt = """
        Create a outline about a cat with superpowers.
        """
    generate_general_story_details(client, prompt)
