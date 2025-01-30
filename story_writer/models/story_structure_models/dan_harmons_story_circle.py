import logging
from typing import Annotated

from pydantic import AfterValidator

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class DanHarmonsStoryCircleStructure(StoryStructure):
    style: str = "Dan Harmon's Story Circle"
    description: str = "A hero's journey type narrative that focuses more on character development."
    you: Annotated[str, AfterValidator(str_not_empty)]
    need: Annotated[str, AfterValidator(str_not_empty)]
    go: Annotated[str, AfterValidator(str_not_empty)]
    search: Annotated[str, AfterValidator(str_not_empty)]
    find: Annotated[str, AfterValidator(str_not_empty)]
    take: Annotated[str, AfterValidator(str_not_empty)]
    returns: Annotated[str, AfterValidator(str_not_empty)]  # Normally "return" but it clashes with python's return.
    change: Annotated[str, AfterValidator(str_not_empty)]
