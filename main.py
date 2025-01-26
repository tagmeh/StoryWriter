from openai import OpenAI

from config.story_settings import STORY_STRUCTURE_STYLE
from story_writer.story.chapters import generate_chapters
from story_writer.story.characters import generate_characters
from story_writer.story.outline import generate_general_story_details
from story_writer.story.scenes import generate_scenes_for_chapter
from story_writer.story.structure import generate_story_structure


if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm studio")

    prompt = """
        Create a story about a cat with superpowers. 
        The cat only has one foot and can throw a football a thousand yards.
        """

    # current_story = "Kilometer Kicker - One-Clawed Triumph - 20250125201724"
    # story_path = story_root = Path(f"stories/{current_story}")

    story_root = generate_general_story_details(client, prompt)
    generate_story_structure(client, story_root, story_structure=STORY_STRUCTURE_STYLE)
    generate_characters(client, story_root)
    generate_chapters(client, story_root)
    generate_scenes_for_chapter(client, story_root)
