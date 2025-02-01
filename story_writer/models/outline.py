import logging
from pathlib import Path
from typing import TypeVar

from story_writer import settings
from story_writer.models.base import CustomBaseModel
from story_writer.models.outline_models import ChapterData, CharacterData, GeneralData, WorldbuildingData
from story_writer.models.outline_models.story_structure_models import (
    ClassicStoryStructure,
    DanHarmonsStoryCircleStructure,
    FichteanCurveStructure,
    FiveActStructure,
    FreytagsPyramidStoryStructure,
    InMediasRes,
    SaveTheCatStructure,
    SevenPointStoryStructure,
    StorySpine,
    TheHerosJourneyStoryStructure,
    ThreeActStructure,
)

log = logging.getLogger(__name__)

CBM = TypeVar("CBM", bound="CustomBaseModel")


class StoryData(CustomBaseModel):
    general: GeneralData | None = None
    structure: (
        ClassicStoryStructure
        | ThreeActStructure
        | FiveActStructure
        | SevenPointStoryStructure
        | FreytagsPyramidStoryStructure
        | TheHerosJourneyStoryStructure
        | DanHarmonsStoryCircleStructure
        | StorySpine
        | FichteanCurveStructure
        | InMediasRes
        | SaveTheCatStructure
        | None
    ) = None
    worldbuilding: WorldbuildingData | None = None
    characters: list[CharacterData] | None = None
    chapters: list[ChapterData] | None = None

    def __str__(self):
        return f"{self.general.title}"

    def save_to_file(self, output_dir: Path, filename: str = None):
        """ output_dir is the path to the story directory /stories/<story>/"""
        if settings.CONSOLIDATE_SAVED_OUTPUT:
            log.debug("Saving story outline data as one consolidated file.")
            super().save_to_file(output_dir=output_dir, filename="story_data")
        else:
            super().save_to_file(output_dir=output_dir, filename="story_data")
            log.debug("Saving story outline data as a series of files in relevant folders.")

            # Save each property separately (dicts as files, lists as files within a directory)
            for key, value in self.model_dump(mode="python").items():
                if value is None:
                    continue  # Prevents creating empty files/folders

                if isinstance(value, list):
                    # Create the subdirectory for the list of x
                    list_dir = output_dir / key
                    list_dir.mkdir(exist_ok=True)
                    print(f"{value=}")
                    for character in self.__getattribute__(key):
                        print(f"{character=}")
                        character.save_to_file(output_dir=list_dir)

                elif isinstance(value, dict):
                    self.__getattribute__(key).save_to_file(output_dir=output_dir, filename=key)

    # TODO: The load feature needs to do one of two things:
    #  1) Try to load the data both ways (consolidated/Not consolidated) because the style of saving can change between stories.
    #  2) Save a settings.json or similar for each story, then reference that to determine style of saving, file_type, ect.
    @classmethod
    def load_from_file(cls: type[CBM], saved_dir: Path, one_file: bool = True):
        # if one_file:
        return super().load_from_file(story_dir=saved_dir, filename="story_data")

        # else:
        #     story_data = {}
        #     for key in ["general", "structure", "worldbuilding"]:
        #         file = saved_dir / f"{key}.{file_type}"
        #         if file.exists():
        #             print(f"{key} {file=}")
        #             story_data[key] = globals()[key.capitalize() + "Data"].load_from_file(
        #                 file_type=file_type, file_path=file
        #             )
        #
        #     char_dir = saved_dir / "characters"
        #     if char_dir.exists():
        #         characters = []
        #         for char_file in char_dir.glob("*.json"):
        #             characters.append(CharacterData.load_from_file(file_type=file_type, file_path=char_file))
        #         story_data["characters"] = characters
        #
        #     chapter_dir = saved_dir / "chapters"
        #     if chapter_dir.exists():
        #         chapters = []
        #         for chapter_subdir in sorted(chapter_dir.iterdir()):
        #             if chapter_subdir.is_dir():
        #                 chapters.append(ChapterData.load_from_file(file_type=file_type, file_path=chapter_subdir))
        #         story_data["chapters"] = chapters
        #
        #     return cls(**story_data)
