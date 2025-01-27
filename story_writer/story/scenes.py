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
    log.debug(f"Generating Scenes for story: {story_data.general.title}")

    # Generate a non-json string block to seed the context before each scene.
    character_seed_str = ""
    for char_dict in [char.dict() for char in story_data.characters]:
        character_seed_str += ", ".join([f"{key}: {val}" for key, val in char_dict.items()])

    model = FIRST_PASS_GENERATION_MODEL
    log.debug(f"Generating Scenes using model: {FIRST_PASS_GENERATION_MODEL}")
    for chapter in story_data.chapters:
        story_structure_seed_str = (
            f"{story_data.structure.style}\n"
            f"{chapter.story_structure_point} - "
            f"{story_data.structure.structure.model_dump(mode='python').get(chapter.story_structure_point.replace(' ', '_').lower(), 'Chapter story structure point not found in generated story structure.')}"
        )

        log.info(f"Generating scenes for chapter {chapter.number}.")
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
        log.debug(f"Number of attempts to generate scenes: {SCENES_PER_CHAPTER_RETRY_COUNT}")
        attempts = 0
        while attempts < max_retries:
            log.debug(f"Attempt {attempts} at generating scenes for chapter {chapter.number}")
            content, elapsed = validated_stream_llm(
                client=client,
                messages=messages,
                model=model,
                response_format=response_format,
                validation_model=SceneData,
            )

            if len(content) < 4:
                log.warning(f"LLM returned fewer than 4 scenes for chapter {chapter.number}. Retrying...")
                attempts += 1
            else:
                log.debug(f"Generated {len(content)} scenes for chapter {chapter.number}.")
                break
        else:
            error = f"Failed to generate at least 4 scenes {chapter.number} in {max_retries} attempts."
            log.exception(error)
            raise RuntimeError(error)

        for count, scene in enumerate(content):
            scene.number = count + 1  # enumerate is zero-based

        chapter.scenes = content

        save_story_data(story_root, story_data)

        utils.log_step(
            story_root=story_root,
            messages=messages,
            file_name=f"generate_scenes_for_chapter_{chapter.number}",
            model=model,
            settings={},
            response_format=response_format,
            duration=elapsed,
        )
    log.info(f"Scenes generated for all chapters. Story outline is complete.")