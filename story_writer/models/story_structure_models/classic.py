import logging
from typing import Annotated

from pydantic import AfterValidator

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class ClassicStoryStructure(StoryStructure):
    # Todo: Update the StoryStructure models to not output the style or description in the model json schema.
    style: str = "Classic Story Structure"
    description: str = "A generic outline structure for all types of stories."
    exposition: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]
