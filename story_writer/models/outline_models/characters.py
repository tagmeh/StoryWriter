import logging
from pathlib import Path
from typing import Annotated, Literal, TypeVar

from pydantic import AfterValidator

from story_writer.models.base import CustomBaseModel
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)

CBM = TypeVar("CBM", bound="CustomBaseModel")


class CharacterData(CustomBaseModel):
    name: Annotated[str, AfterValidator(str_not_empty)]
    age: Annotated[str, AfterValidator(str_not_empty)]
    role: Annotated[str, AfterValidator(str_not_empty)]
    description: Annotated[str, AfterValidator(str_not_empty)]
    personality: Annotated[str, AfterValidator(str_not_empty)]

    def __iter__(self):
        return iter(self)

    def save_to_file(self, output_dir: Path, file_type: Literal["json", "yaml"], filename: str = None):
        super().save_to_file(output_dir=output_dir, file_type=file_type, filename=f"{self.name}")

    @classmethod
    def load_from_file(cls: type[CBM], file_type: Literal["json", "yaml"], file_path: Path) -> CBM:
        return super().load_from_file(file_path=file_path, file_type=file_type)
