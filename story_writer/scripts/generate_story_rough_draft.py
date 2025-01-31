import logging
from pathlib import Path

from openai import Client

from story_writer.models.outline import StoryData

log = logging.getLogger(__name__)


def generate_story_rough_draft(client: Client, title: str):
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
    project_root = Path(__file__).parents[2]  # ../StoryWriter/
    print(f"{project_root=}")
    story_root = Path(f"{project_root}/stories/{title}")

    if not story_root.exists:
        log.error(f"Story '{title}' does not exist at {story_root}.")

    # TODO: Consider renaming StoryData to Outline or something similar? OutlineData.
    story_data: StoryData = StoryData.load_from_file(saved_dir=story_root)

    # Generate a system message that contains the basic background information on the story.
    # Title, themes, genres

    for chapter in story_data.chapters:
        """
        title: Annotated[str, AfterValidator(str_not_empty)]
        number: int | None = None  # This is added manually. LLMs don't always count in order.
        story_structure_point: Annotated[str, AfterValidator(str_not_empty)]
        location: Annotated[str, AfterValidator(str_not_empty)]
        characters: list[ChapterCharacterData]
        synopsis: Annotated[str, AfterValidator(str_not_empty)]
        scenes: list[SceneData] = []
        """

        # Chapter information
        # title
        # number/total (May help indicate to the model where we're at in the story)
        # Current story structure point
        #   then extract that information from the story_structure object.
        # location (Still on the fence if I should add a section fleshing out the locations)
        # Characters as a list of strings
        #   Characters' personality and details based on who is in this chapter/scenes
        # Synoposis

        for scene in chapter.scenes:
            """
            summary: Annotated[str, AfterValidator(str_not_empty)]
            number: int | None = None  # This is added manually. LLMs don't always count in order.
            characters: list[SceneCharacterdata]
                name: Annotated[str, AfterValidator(str_not_empty)]

                status: Annotated[str, AfterValidator(str_not_empty)]
            location: Annotated[str, AfterValidator(str_not_empty)]
            misc: str | None = None
            story_beats: list[Annotated[str, AfterValidator(str_not_empty)]]
            """

        ...
