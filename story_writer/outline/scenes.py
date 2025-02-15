import logging

from openai import Client

from story_writer import settings
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import SceneData
from story_writer.prompts import generate_story_chapter_scene_prompt

log = logging.getLogger(__name__)


def generate_scenes_for_chapter(client: Client):
    """
    For each chapter, generate a few scenes based on the chapter synopsis, location, and characters.
    """
    story_data: StoryData = StoryData.load_from_file(saved_dir=settings.story_dir)
    log.debug(f"Generating Scenes for outline: {story_data.general.title}")

    # Generate a non-json string block to seed the context before each scene.
    character_seed_str = "".join([c.list_key_values_str() for c in story_data.characters])

    log.debug(f"Generating Scenes using model: {settings.llm.model}")
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
            {"role": "system", "content": settings.basic_system_prompt},
            {
                "role": "user",
                "content": f"Characters: \n{character_seed_str}\nStory Structure/Outline: {story_structure_seed_str}",
            },
            {
                "role": "user",
                "content": generate_story_chapter_scene_prompt(story_data, chapter),
            },
        ]

        max_retries = settings.scenes_per_chapter_retry_count
        log.debug(f"Number of attempts to generate scenes: {settings.scenes_per_chapter_retry_count}")
        attempts = 0
        while attempts < max_retries:
            log.debug(f"Attempt {attempts} at generating scenes for chapter {chapter.number}")
            content, elapsed = get_validated_llm_output(
                client=client,
                messages=messages,
                validation_model=SceneData,
                model_settings=settings.stage.scenes,
                log_file_name=f"generate_scenes_for_chapter_{chapter.number}",
            )

            if len(content) < settings.scenes_per_chapter_minimum_count:
                log.warning(
                    f"LLM returned fewer than {settings.scenes_per_chapter_minimum_count} "
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

        story_data.save_to_file(output_dir=settings.story_dir)

        # utils.log_step(
        #     story_root=story_root,
        #     messages=messages,
        #     file_name=f"generate_scenes_for_chapter_{chapter.number}",
        #     model=model,
        #     settings={},
        #     response_model=SceneData,
        #     duration=elapsed,
        # )
    log.info("Scenes generated for all chapters. Story outline is complete.")
