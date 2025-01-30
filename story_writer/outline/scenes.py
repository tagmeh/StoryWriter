import logging
from pathlib import Path

from openai import Client

from story_writer import settings, utils
from story_writer.config.models import FIRST_PASS_GENERATION_MODEL
from story_writer.config.prompts import generate_story_chapter_scene_prompt
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import SceneData

# from story_writer.utils import load_story_data, save_story_data

log = logging.getLogger(__name__)


def generate_scenes_for_chapter(client: Client, story_root: Path):
    """
    For each chapter, generate a few scenes based on the chapter synopsis, location, and characters.
    """
    # story_data: StoryData = load_story_data(story_path=story_root)
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)
    log.debug(f"Generating Scenes for outline: {story_data.general.title}")

    # Generate a non-json string block to seed the context before each scene.
    character_seed_str = "".join([c.list_key_values_str() for c in story_data.characters])

    model = FIRST_PASS_GENERATION_MODEL
    log.debug(f"Generating Scenes using model: {FIRST_PASS_GENERATION_MODEL}")
    for chapter in story_data.chapters:
        story_structure_seed_str = (
            f"{story_data.structure.style}\n"
            f"{chapter.story_structure_point} - "
            # Get only the relevant story structure point.
            # Uses a normalized story structure style to pull the correct section.
            f"{story_data.structure.model_dump(mode='python').get(chapter.story_structure_point.replace(' ', '_').lower(), 'Chapter outline structure point not found in generated outline structure.')}"
        )

        log.info(f"Generating scenes for chapter {chapter.number}.")
        messages = [
            {"role": "system", "content": settings.BASIC_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Characters: \n{character_seed_str}\nStory Structure/Outline: {story_structure_seed_str}",
            },
            {
                "role": "user",
                "content": generate_story_chapter_scene_prompt(story_data, chapter),
            },
        ]

        max_retries = settings.SCENES_PER_CHAPTER_RETRY_COUNT
        log.debug(f"Number of attempts to generate scenes: {settings.SCENES_PER_CHAPTER_RETRY_COUNT}")
        attempts = 0
        while attempts < max_retries:
            log.debug(f"Attempt {attempts} at generating scenes for chapter {chapter.number}")
            content, elapsed = get_validated_llm_output(
                client=client,
                messages=messages,
                model=settings.STAGE.SCENES.model,
                temperature=settings.STAGE.SCENES.temperature,
                max_tokens=settings.STAGE.SCENES.max_tokens,
                validation_model=SceneData,
            )

            if len(content) < settings.SCENES_PER_CHAPTER_MINIMUM_COUNT:
                log.warning(
                    f"LLM returned fewer than {settings.SCENES_PER_CHAPTER_MINIMUM_COUNT} "
                    f"scenes for chapter {chapter.number}. This is a user-setting. If the LLM model "
                    f"continues to fail, try updating the scene-generator prompt or lowering the minimum "
                    f"scenes per chapter in config/story_settings.py - SCENES_PER_CHAPTER_MINIMUM_COUNT. "
                    f"Retrying..."
                )
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

        # save_story_data(story_root, story_data)
        story_data.save_to_file(output_dir=story_root)

        utils.log_step(
            story_root=story_root,
            messages=messages,
            file_name=f"generate_scenes_for_chapter_{chapter.number}",
            model=model,
            settings={},
            response_model=SceneData,
            duration=elapsed,
        )
    log.info("Scenes generated for all chapters. Story outline is complete.")
