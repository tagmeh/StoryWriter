import logging
from typing import Annotated

from pydantic import AfterValidator, Field
from pydantic.json_schema import SkipJsonSchema

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class InMediasRes(StoryStructure):
    style: SkipJsonSchema[str] = "In Medias Res"
    description: SkipJsonSchema[str] = "Framework for starting the outline in the middle of the action."
    in_medias_res: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Starts off immediately in the action with little to no exposition or backstory."),
    ]
    rising_action: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Conflict increases, characters have to adjust. Still don't know everything going on at this time."
        ),
    ]
    explanation: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Rest point where exposition or backstory informs the reader what or why things are happening."
        ),
    ]
    climax: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Everything comes together and the protagonist succeeds or fails."),
    ]
    falling_action: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="All loose ends are tied up and the reader is allowed to breathe."),
    ]
    resolution: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Protagonist returns to their ordinary world and plot threads are addressed."),
    ]
