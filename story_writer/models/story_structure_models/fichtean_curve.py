import logging
from typing import Annotated

from pydantic import AfterValidator
from pydantic.json_schema import SkipJsonSchema

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class FichteanCurveStructure(StoryStructure):
    style: SkipJsonSchema[str] = "Fichtean Curve"
    description: SkipJsonSchema[str] = (
        "Packed with tension and mini-crises, the protagonist goes through multiple "
        "obstacles along their journey. Bypasses the 'ordinary world' setup."
    )
    inciting_incident: Annotated[str, AfterValidator(str_not_empty)]
    first_crisis: Annotated[str, AfterValidator(str_not_empty)]
    second_crisis: Annotated[str, AfterValidator(str_not_empty)]
    third_crisis: Annotated[str, AfterValidator(str_not_empty)]
    fourth_crisis: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
