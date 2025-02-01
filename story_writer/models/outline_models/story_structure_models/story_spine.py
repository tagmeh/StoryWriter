import logging
from typing import Annotated

from pydantic import AfterValidator, Field
from pydantic.json_schema import SkipJsonSchema

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class StorySpine(StoryStructure):
    style: SkipJsonSchema[str] = "Story Spine"
    description: SkipJsonSchema[str] = ""
    once_upon_a_time: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Setup protagonist and the starting situation.")
    ]
    and_every_day: Annotated[
        str, AfterValidator(str_not_empty), Field(description="More exposition, describing the status quo.")
    ]
    until_one_day: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Inciting incident to shake things up.")
    ]
    and_because_of_this: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Protagonists are forced to leave their normal lives and go on an adventure."),
    ]
    and_then: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="The pursuit of their goals have consequences. A goal may have been achieved, but it leads to something else."
        ),
    ]
    until_finally: Annotated[str, AfterValidator(str_not_empty), Field(description="Climax of the outline.")]
    and_ever_since_that_day: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="How did the hero change from the journey. What did they bring back with them."),
    ]
