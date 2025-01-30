import logging
from typing import Annotated

from pydantic import AfterValidator, Field

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class ThreeActStructure(StoryStructure):
    style: str = "Three Act Structure"
    description: str = (
        "Traditional outline structure, most structures follow a variation on this one. Very popular in movies"
    )
    act_1_exposition: Annotated[str, AfterValidator(str_not_empty), Field(description="Establish the status quo.")]
    act_1_inciting_incident: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Event that starts the outline.")
    ]
    act_1_plot_point_1: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist has decided to deal with the conflict.")
    ]
    act_2_rising_action: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The hero is beset with various challenges that increase the stakes in the tension."),
    ]
    act_2_midpoint: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="An event that turns everything on its head, nearly ruining the protagonist's chances of achieving their goal."
        ),
    ]
    act_2_plot_point_2: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Following the midpoint, the protagonist fails at a challenge. Protagonist may question capability of succeeding."
        ),
    ]
    act_3_pre_climax: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Protagonist pulls themself together and prepares for the final confrontation."),
    ]
    act_3_climax: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The final confrontation between the protagonist and antagonist. Protagonist usually wins."),
    ]
    act_3_denouement: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="All loose ends are neatly tied up, consequences of the climax are clearly spelled out."),
    ]
