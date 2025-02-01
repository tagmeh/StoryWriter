import json
import logging
from pathlib import Path
from typing import Annotated, Literal, TypeVar

import yaml
from pydantic import AfterValidator
from pydantic.json_schema import SkipJsonSchema

from story_writer import settings
from story_writer.models.base import CustomBaseModel
from story_writer.models.outline_models.scenes import SceneData
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)

CBM = TypeVar("CBM", bound="CustomBaseModel")


class ChapterCharacterData(CustomBaseModel):
    # Todo: Identify a better way to capture chapter/scene char data to relate it to the generated characters.
    name: Annotated[str, AfterValidator(str_not_empty)]
    status: Annotated[str, AfterValidator(str_not_empty)]


class ChapterData(CustomBaseModel):
    title: Annotated[str, AfterValidator(str_not_empty)]
    # Overwritten after the chapters are created. LLMs don't always count in order.
    # Left here to discourage title names with the chapter number in them. eg "Chapter Two: Camelot"
    number: int
    story_structure_point: Annotated[str, AfterValidator(str_not_empty)]
    location: Annotated[str, AfterValidator(str_not_empty)]
    characters: list[ChapterCharacterData]
    synopsis: Annotated[str, AfterValidator(str_not_empty)]
    scenes: SkipJsonSchema[list[SceneData]] = []

    def save_to_file(self, output_dir: Path, filename: str = None):
        """
        :param output_dir: This is the /chapterdata/ directory
        :param filename:
        :return: None, creates a /Chapter-n/ directory and saves the chapter and scenes within that dir.
        """
        chapter_dir = output_dir / f"Chapter-{self.number}"
        chapter_dir.mkdir(exist_ok=True)
        super().save_to_file(output_dir=chapter_dir, filename=f"chapter-{self.number}")

        if self.scenes:
            for scene in self.scenes:
                scene.save_to_file(output_dir=chapter_dir, filename=f"scene-{self.number}")

    @classmethod
    def load_from_file(cls: type[CBM], file_path: Path) -> CBM:
        # Load chapter data
        print(f"chapter file path {file_path=}")
        chapter_file = file_path / f"chapter-{file_path.name.split('-')[-1]}.{settings.SAVE_STORY_FILE_TYPE}"
        if settings.SAVE_STORY_FILE_TYPE == "json":
            with open(chapter_file, encoding="utf-8") as f:
                chapter_data = json.load(f)
        elif settings.SAVE_STORY_FILE_TYPE == "yaml":
            with open(chapter_file, encoding="utf-8") as f:
                chapter_data = yaml.safe_load(f)
        else:
            raise Exception(f"File type: '{settings.SAVE_STORY_FILE_TYPE}' not supported.")

        scenes = []
        for scene_path in sorted(file_path.glob(f"scene-*.{settings.SAVE_STORY_FILE_TYPE}")):
            print(f"{scene_path=}")
            scenes.append(SceneData.load_from_file(story_dir=scene_path))

        # TODO: Know that the scenes are still saved with the chapter.
        #  Possible way of going about it, solution?, is to save the scenes then clear them from the chapter,
        #  maybe with a message indicating the files are saved separately.
        chapter_data["scenes"] = scenes

        return cls(**chapter_data)
