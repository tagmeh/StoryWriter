import logging
from pathlib import Path
from typing import Annotated, Literal, TypeVar

from pydantic import AfterValidator, BaseModel

from story_writer.models.base import CustomBaseModel
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
CBM = TypeVar("CBM", bound="CustomBaseModel")


class SceneCharacterdata(CustomBaseModel):
    name: Annotated[str, AfterValidator(str_not_empty)]
    status: Annotated[str, AfterValidator(str_not_empty)]


class SceneData(CustomBaseModel):
    summary: Annotated[str, AfterValidator(str_not_empty)]
    number: int | None = None  # This is added manually. LLMs don't always count in order.
    characters: list[SceneCharacterdata]
    location: Annotated[str, AfterValidator(str_not_empty)]
    misc: str | None = None
    story_beats: list[Annotated[str, AfterValidator(str_not_empty)]]

    def save_to_file(self, output_dir: Path, file_type: Literal["json", "yaml"], filename: str = None):
        super().save_to_file(output_dir=output_dir, file_type=file_type, filename=filename)
