import logging
from typing import Annotated

from pydantic import AfterValidator, Field

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class FreytagsPyramidStoryStructure(StoryStructure):
    style: str = "Freytag's Pyramid"
    description: str = "A outline structure for tragic narratives."
    exposition: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Establish the status quo. Ends with the inciting incident."),
    ]
    rising_action: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist pursues their goal as the stakes rise.")
    ]
    climax: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Center of the outline, the point of no return.")
    ]
    falling_action: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="We see the consequences of the climax. In a tragedy, things start to spiral out of control."
        ),
    ]
    denouement: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Everything is wrapped up. In a tragedy, the protagonist is at their lowest point."),
    ]
