import logging

from openai import Client

from story_writer import settings
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import ChapterData
from story_writer.prompts import generate_story_chapters_prompt

log = logging.getLogger(__name__)


def generate_chapters(client: Client):
    story_data: StoryData = StoryData.load_from_file(saved_dir=settings.story_dir)

    character_seed_str = ""
    for char_dict in [char.dict() for char in story_data.characters]:
        character_seed_str += ", ".join([f"{key}: {val}" for key, val in char_dict.items()])

    messages = [
        {"role": "system", "content": settings.basic_system_prompt},
        {  # Seed data prior to chapter-generation instructions.
            "role": "user",
            "content": f"Story characters:\n{character_seed_str}",
        },
        {"role": "user", "content": generate_story_chapters_prompt(story_data)},
    ]

    content, elapsed = get_validated_llm_output(
        client=client,
        messages=messages,
        validation_model=ChapterData,
        model_settings=settings.stage.chapters,
        log_file_name="generate_chapters",
    )

    for count, chapter in enumerate(content):
        chapter.number = count + 1  # enumerate is zero-based

    story_data.chapters = content

    log.debug("Saving Chapter Outline Data.")
    story_data.save_to_file(output_dir=settings.story_dir)

    # utils.log_step(
    #     story_root=story_root,
    #     file_name="generate_chapters",
    #     messages=messages,
    #     model=model,
    #     settings={},
    #     response_model=ChapterData,
    #     duration=elapsed,
    # )
