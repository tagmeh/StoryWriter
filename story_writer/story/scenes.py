from pathlib import Path

import yaml
from openai import Client

from config.models import FIRST_PASS_GENERATION_MODEL
from config.prompts import GENERAL_SYSTEM_PROMPT, generate_story_chapter_scene_prompt
from config.story_settings import SCENES_PER_CHAPTER_RETRY_COUNT
from story_writer import utils
from story_writer.llm import validated_stream_llm
from story_writer.response_schemas import story_chapter_scene_schema
from story_writer.story_data_model import StoryData, SceneData


def generate_scenes_for_chapter(client: Client, story_root: Path):
    """
    For each chapter, generate a few scenes based on the chapter synopsis, location, and characters.
    """
    # Load story-specific content.
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = StoryData(**yaml.safe_load(f))

    # Generate a non-json string block to seed the context before each scene.
    character_seed_str = ""
    for char_dict in [char.dict() for char in story_data.characters]:
        character_seed_str += ", ".join(
            [f"{key}: {val}" for key, val in char_dict.items()]
        )

    story_structure_seed_str = "\n".join(
        [
            f"{key}: {val}"
            for key, val in story_data.structure.model_dump(mode="python").items()
        ]
    )
    # End of context-seeding instructions

    model = FIRST_PASS_GENERATION_MODEL
    for chapter in story_data.chapters:
        print(f"Generating scenes for chapter {chapter.chapter_number}.")
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
        for attempts in range(max_retries):
            content, elapsed = validated_stream_llm(
                client=client,
                messages=messages,
                model=model,
                response_format=response_format,
                validation_model=SceneData,
            )

            if len(content) > 4:
                print(
                    f"LLM returned fewer than 4 scenes for chapter {chapter.chapter_number}. Retry..."
                )
                break
        else:
            raise Exception(
                f"Failed to generate at least 4 scenes per chapter {chapter.chapter_number} "
                f"in {max_retries} attempts."
            )

        chapter.scenes = content

        with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
            yaml.dump(
                story_data.model_dump(mode="python"),
                f,
                default_flow_style=False,
                sort_keys=False,
            )

        file_name = f"generate_scenes_for_chapter_{chapter.chapter_number}"
        utils.log_step(
            story_root=story_root,
            messages=messages,
            file_name=file_name,
            model=model,
            settings={},
            response_format=response_format,
            duration=elapsed,
        )
