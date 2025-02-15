import logging
from typing import Annotated

from pydantic import AfterValidator

from story_writer.models.base import CustomBaseModel
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class WorldbuildingData(CustomBaseModel):
    # Todo: Create a validator to validate that some of these fields are filled out.
    #  I don't think all of them have to be filled out for every story, but at least some should.
    geography: str | None = None
    culture: Annotated[str, AfterValidator(str_not_empty)]
    history: str | None = None
    politics: str | None = None
    economy: str | None = None
    magic_technology: str | None = None
    religion: str | None = None
    additional_details: Annotated[str, AfterValidator(str_not_empty)]
