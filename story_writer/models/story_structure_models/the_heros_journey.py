import logging
from typing import Annotated

from pydantic import AfterValidator, Field

from story_writer.models.base import StoryStructure
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class TheHerosJourneyStoryStructure(StoryStructure):
    style: str = "The Hero's Journey"
    description: str = (
        "Campbell’s original structure uses terminology that lends itself well to epic tales of bravery and triumph."
    )
    the_ordinary_world: Annotated[
        str, AfterValidator(str_not_empty), Field(description="The hero’s everyday life is established.")
    ]
    the_call_to_adventure: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Otherwise known as the inciting incident.")
    ]
    the_refusal_of_the_call: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="For a moment, the hero is reluctant to take on the challenge."),
    ]
    meeting_the_mentor: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Our hero meets someone who prepares them for what lies ahead."),
    ]
    crossing_the_threshold: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The hero steps out of their comfort zone and enters a ‘new world.’"),
    ]
    tests_allies_enemies: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Our protagonist faces new challenges, and maybe picks up some new friends."),
    ]
    approach_to_the_inmost_cave: Annotated[
        str, AfterValidator(str_not_empty), Field(description="The hero gets close to their goal.")
    ]
    the_ordeal: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The hero meets (and overcomes) their greatest challenge yet."),
    ]
    seizing_the_sword: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The hero obtains something important they were after, and victory is in sight."),
    ]
    the_road_back: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="The hero realizes that achieving their goal is not the final hurdle."),
    ]
    resurrection: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(
            description="The hero faces their final challenge — a climactic test that hinges on everything they’ve learned over their journey."
        ),
    ]
    return_with_the_elixir: Annotated[
        str,
        AfterValidator(str_not_empty),
        Field(description="Having triumphed, our protagonist returns to their old life. "),
    ]
