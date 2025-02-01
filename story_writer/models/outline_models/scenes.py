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
    # Todo: Identify a better way to capture chapter/scene char data to relate it to the generated characters.
    name: Annotated[str, AfterValidator(str_not_empty)]
    # Todo: Consider adding a description or field to try and keep the name field clean.
    #  Can get values like "Alice (some other nonsense)"
    #  Can also get statuses that just explain what the character is doing or feeling.
    status: Annotated[str, AfterValidator(str_not_empty)]


class SceneData(CustomBaseModel):
    summary: Annotated[str, AfterValidator(str_not_empty)]
    number: int | None = None  # This is added manually. LLMs don't always count in order.
    characters: list[SceneCharacterdata]
    location: Annotated[str, AfterValidator(str_not_empty)]
    misc: str | None = None
    story_beats: list[Annotated[str, AfterValidator(str_not_empty)]]

    def save_to_file(self, output_dir: Path, filename: str = None):
        super().save_to_file(output_dir=output_dir, filename=filename)
