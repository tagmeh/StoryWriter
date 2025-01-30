import logging
from typing import Annotated

from pydantic import AfterValidator

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class SevenPointStoryStructure(StoryStructure):
    style: str = "Seven Point Story Structure"
    description: str = ""
    hook: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_1: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_1: Annotated[str, AfterValidator(str_not_empty)]
    mid_point: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_2: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_2: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]
