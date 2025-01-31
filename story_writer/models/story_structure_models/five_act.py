import logging
from typing import Annotated

from pydantic import AfterValidator, Field
from pydantic.json_schema import SkipJsonSchema

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class FiveActStructure(StoryStructure):
    style: SkipJsonSchema[str] = "Five Act Structure"
    description: SkipJsonSchema[str] = "Basically the same as Freytag's Pyramid, but without the expectation of it being a tragedy."
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
    resolution: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Everything is wrapped up. The protagonist is usually at their highest point."),
    ]
