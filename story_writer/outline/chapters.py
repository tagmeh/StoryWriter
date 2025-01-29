from pathlib import Path

from openai import Client

from story_writer.config.models import FIRST_PASS_GENERATION_MODEL
from story_writer.config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_chapters_prompt
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.story_data_model import ChapterData, StoryData


def generate_chapters(client: Client, story_root: Path):
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)

    character_seed_str = ""
    for char_dict in [char.dict() for char in story_data.characters]:
        character_seed_str += ", ".join([f"{key}: {val}" for key, val in char_dict.items()])

    model = FIRST_PASS_GENERATION_MODEL
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {  # Seed data prior to chapter-generation instructions.
            "role": "user",
            "content": f"Story characters:\n{character_seed_str}",
        },
        {"role": "user", "content": generate_story_chapters_prompt(story_data)},
    ]

    content, elapsed = validated_stream_llm(
        client=client,
        messages=messages,
        model=model,
        validation_model=ChapterData,
    )

    for count, chapter in enumerate(content):
        chapter.number = count + 1  # enumerate is zero-based

    story_data.chapters = content

    story_data.save_to_file(output_dir=story_root)

    utils.log_step(
        story_root=story_root,
        messages=messages,
        file_name="generate_chapters",
        model=model,
        settings={},
        response_model=ChapterData,
        duration=elapsed,
    )
