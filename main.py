from openai import OpenAI
from story_writer.story.outline import generate_general_story_details
from story_writer.story.structure import generate_story_structure
from story_writer.story_structures import StoryStructure

# from story_writer.tui.app import MainPageApp
#
# if __name__ == '__main__':
#     app = MainPageApp()
#     app.run()

if __name__ == '__main__':
    client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

    prompt = """
        Create a story about a cat with superpowers. The cat only has one foot and can throw a football a thousand yards.
        """

    story_root = generate_general_story_details(client, prompt)
    generate_story_structure(client, story_root, story_structure=StoryStructure.SEVEN_POINT)
