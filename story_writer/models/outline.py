import json
import logging
from pathlib import Path
from typing import Literal, TypeVar

import yaml

from story_writer.models.base import CustomBaseModel
from story_writer.models.outline_models import ChapterData, CharacterData, GeneralData, WorldbuildingData
from story_writer.models.story_structure_models import (
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

    def save_to_file(
        self, output_dir: Path, file_type: Literal["json", "yaml"] = "yaml", one_file: bool = True, filename: str = None
    ):
        """
        Saves the StoryData output depending on a couple of settings.
        :param output_dir: Should be /stories/
        :param file_type: json or yaml, based on user setting.
        :param filename: None
        :param one_file: bool - If True, saves the StoryData data as one file: "story_data.*" Otherwise, save files separately
        :return:
        """
        # story_dir = output_dir / self.general.title
        story_dir = output_dir
        story_dir.mkdir(parents=True, exist_ok=True)

        # if one_file:
        # Save the data into one file as either a json or yaml file.
        story_data_path = story_dir / f"story_data.{file_type}"
        log.debug(f"Saving/Updating outline data to {story_data_path}")

        if file_type == "yaml":
            with open(story_data_path, mode="w+", encoding="utf-8") as f:
                yaml.dump(self.model_dump(mode="python"), f, default_flow_style=False, sort_keys=False)

        elif file_type == "json":
            with open(story_data_path, mode="w+", encoding="utf-8") as f:
                json.dump(self.model_dump(mode="json"), f, indent=4, sort_keys=False)

        else:
            log.error(f"Failed to save story data, save type is invalid: {file_type}")

        # else:
        #     # Save each property separately (dicts as files, lists as files within a directory)
        #     for key, value in self.model_dump(mode="python").items():
        #         if value is None:
        #             continue  # Prevents creating empty files/folders
        #
        #         if isinstance(value, list):
        #             # Create the subdirectory for the list of x
        #             list_dir = story_dir / key
        #             list_dir.mkdir(exist_ok=True)
        #             print(f"{value=}")
        #             for character in self.__getattribute__(key):
        #                 print(f"{character=}")
        #                 character.save_to_file(output_dir=list_dir, file_type=file_type)
        #
        #         elif isinstance(value, dict):
        #             self.__getattribute__(key).save_to_file(
        #                 output_dir=story_dir, file_type=file_type, filename=f"{key}"
        #             )

    # TODO: The load feature needs to do one of two things:
    #  1) Try to load the data both ways (consolidated/Not consolidated) because the style of saving can change between stories.
    #  2) Save a settings.json or similar for each story, then reference that to determine style of saving, file_type, ect.
    @classmethod
    def load_from_file(
        cls: type[CBM], saved_dir: Path, file_type: Literal["json", "yaml"] = "yaml", one_file: bool = True
    ) -> "StoryData":
        # if one_file:
        story_data_path = saved_dir / f"story_data.{file_type}"
        log.debug(f"Loading outline data from '{story_data_path}'")

        if file_type == "yaml":
            with open(story_data_path, encoding="utf-8") as f:
                return StoryData(**yaml.safe_load(f))

        elif file_type == "json":
            with open(story_data_path, encoding="utf-8") as f:
                return StoryData(**json.load(fp=f))
        else:
            log.error(f"Failed to load story data, save type is invalid: {file_type}")

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
