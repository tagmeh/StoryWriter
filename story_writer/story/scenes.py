import logging
from pathlib import Path

from openai import Client

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_chapter_scene_prompt
from config.story_settings import SCENES_PER_CHAPTER_RETRY_COUNT
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.response_schemas import story_chapter_scene_schema
from story_writer.story_data_model import SceneData, StoryData
from story_writer.utils import load_story_data, save_story_data

log = logging.getLogger(__name__)


def generate_scenes_for_chapter(client: Client, story_root: Path):
    """
    For each chapter, generate a few scenes based on the chapter synopsis, location, and characters.
    """
    story_data: StoryData = load_story_data(story_path=story_root)

    # Generate a non-json string block to seed the context before each scene.
    character_seed_str = ""
    for char_dict in [char.dict() for char in story_data.characters]:
        character_seed_str += ", ".join([f"{key}: {val}" for key, val in char_dict.items()])

    model = FIRST_PASS_GENERATION_MODEL
    for chapter in story_data.chapters:
        story_structure_seed_str = (
            f"{story_data.structure.style}\n"
            f"{chapter.story_structure_point} - "
            f"{story_data.structure.structure.model_dump(mode='python').get(chapter.story_structure_point.replace(' ', '_').lower(), 'Chapter story structure point not found in generated story structure.')}"
        )

        print(f"Generating scenes for chapter {chapter.number}.")
        messages = [
            {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Characters: \n{character_seed_str}\nStory Structure/Outline: {story_structure_seed_str}",
            },
            {
                "role": "user",
                "content": generate_story_chapter_scene_prompt(story_data, chapter),
            },
        ]
        response_format: dict = story_chapter_scene_schema

        max_retries = SCENES_PER_CHAPTER_RETRY_COUNT
        attempts = 0
        while attempts < max_retries:
            content, elapsed = validated_stream_llm(
                client=client,
                messages=messages,
                model=model,
                response_format=response_format,
                validation_model=SceneData,
            )

            if len(content) < 4:
                print(f"LLM returned fewer than 4 scenes for chapter {chapter.number}. Retry...")
                attempts += 1
            else:
                log.debug(f"Generated {len(content)} scenes for chapter {chapter.number}.")
                break
        else:
            raise Exception(f"Failed to generate at least 4 scenes {chapter.number} in {max_retries} attempts.")

        for count, scene in enumerate(content):
            scene.number = count

        chapter.scenes = content

        save_story_data(story_root, story_data)

        file_name = f"generate_scenes_for_chapter_{chapter.number}"
        utils.log_step(
            story_root=story_root,
            messages=messages,
            file_name=file_name,
            model=model,
            settings={},
            response_format=response_format,
            duration=elapsed,
        )
