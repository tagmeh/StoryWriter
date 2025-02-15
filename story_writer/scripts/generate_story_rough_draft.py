import logging

from openai import Client

from story_writer import llm, settings
from story_writer.models.outline import StoryData

log = logging.getLogger(__name__)


def generate_story_rough_draft(client: Client):
    """
    Using the story outline data, iterate over each scene in each chapter, seeding the context with story details.

    Initial implementation will attempt to generate one chapter at a time, scene by scene. Using the previous scene(s)
    as context for the next scene. Other context will be relevant character details per the scene and also the
    overarching or more generalized story data.

    The goal of this script is to output a semi-coherent story.

    :client: Client - OpenAI Client object used to generate chat completions with the LLM platform of choice.
    :title: str - Story name as it appears in the /stories/ directory (Including timestamp)
        ex. "Clawed Heroine - The Rise of Lila Leclair - 1738285520077"
    """
    # project_root = Path(__file__).parents[2]  # ../StoryWriter/
    # print(f"{project_root=}")
    # story_root = Path(f"{project_root}/stories/{title}")
    # print(f"{story_root=}")
    #
    # if not story_root.exists:
    #     log.error(f"Story '{title}' does not exist at {story_root}.")

    # TODO: Consider renaming StoryData to Outline or something similar? OutlineData.
    # story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)
    story_data: StoryData = StoryData.load_from_file(saved_dir=settings.story_dir)

    for chapter in story_data.chapters:

        scene_draft_array = []
        for scene in chapter.scenes:
            prompt = f"""
                Expand on the scene's story beats, creating a rough draft. Elaborate, add detail, and dialogue.
                            
                Themes: {", ".join(story_data.general.themes)}
                Genre: {", ".join(story_data.general.genres)}
                Synopsis: {story_data.general.synopsis}
                
                Chapter {chapter.number}
                Chapter Synopsis: {chapter.synopsis}
                Chapter Story Point: {chapter.story_structure_point}
                
                Relevant Story Structure: {story_data.structure.model_dump().get(chapter.story_structure_point, 'Failed to get story structure point details.')}
                
                Scene {scene.number}
                Characters in scene: {", ".join([f"{char.name}: {char.status}" for char in scene.characters])}          
                Scene Location: {scene.location}
                Scene Story Beats: {", ".join(scene.story_beats)}         
            """
            character_seed_str = ""
            for char_dict in [char.dict() for char in story_data.characters]:
                character_seed_str += ", ".join([f"{key}: {val}" for key, val in char_dict.items()])

            messages = [
                {"role": "system", "content": settings.basic_system_prompt},
                {"role": "user", "content": f"Story characters:\n{character_seed_str}"},
                {"role": "user", "content": prompt},
            ]

            scene_draft_array.append(
                llm.get_validated_llm_output(
                    client=client, messages=messages, log_file_name="first-draft", model_settings=settings.draft
                )
            )

        chapter_draft = f"{chapter.title}\n\n  ********************  \n\n"
        for scene_draft in scene_draft_array:
            chapter_draft += f"{scene_draft}\n\n\n  ********************  \n\n"

        file_path = settings.story_dir / "draft" / f"Chapter-{chapter.number}.txt"
        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(chapter_draft)


if __name__ == "__main__":
    import argparse

    from openai import OpenAI


    print(settings.story_dir)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        type=str,
        default="1234",
    )
    parser.add_argument("--host", type=str, default="http://127.0.0.1")
    parser.add_argument("--api-key", type=str, default="story-writer")
    args = parser.parse_args()

    client = OpenAI(base_url=f"{args.host}:{args.port}/v1", api_key=args.api_key)
    generate_story_rough_draft(client=client)
