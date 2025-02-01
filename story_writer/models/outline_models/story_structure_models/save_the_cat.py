import logging
from typing import Annotated

from pydantic import AfterValidator, Field
from pydantic.json_schema import SkipJsonSchema

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class SaveTheCatStructure(StoryStructure):
    style: SkipJsonSchema[str] = "Save the Cat"
    description: SkipJsonSchema[str] = "A more detailed version of the three act structure."
    opening_image: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Story starts out with a brief look at the protagonist, gets the feel and tone of the outline."
        ),
    ]
    set_up: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="A little more exposition, setup the tone of the world, introduce the characters."),
    ]
    theme_stated: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Make clear what the theme is. The theme may becomes more obvious to the progatonist as the outline progresses."
        ),
    ]
    catalyst: Annotated[
        str, AfterValidator(str_not_empty), Field(description="The inciting incident. The journey begins.")
    ]
    debate: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Protagonist fights or debates with the path they have taken."),
    ]
    break_into_two: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist is fully invested in their quest.")
    ]
    b_story: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Introduced to the b plot of the outline.")
    ]
    fun_and_games: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Protagonist enjoys a small amount of time to enjoy their new life, world, and abilities they have gained."
        ),
    ]
    midpoint: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Something happens to turn the everything on its head.")
    ]
    bad_guys_close_in: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The antagonist's forces become a greater threat to the protagonist."),
    ]
    all_is_lost: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Something happens to the protagonist and puts them under extreme duress. "),
    ]
    dark_night_of_the_soul: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The protagonist goes through a depressive period when it seems all hope is lost."),
    ]
    break_into_three: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="Protagonist rises up from rock bottom and gains a key piece of knowledge that helps them in the future."
        ),
    ]
    finale: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Protagonist takes what they have learned from their journey to defeat the antagonist."),
    ]
    final_image: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The final snapshot of the outline, it should mirror the opening image."),
    ]
