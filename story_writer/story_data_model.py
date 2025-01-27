import re
from typing import Any, TypeVar, Type, Generic, Annotated, Union

from pydantic import BaseModel, field_validator, AfterValidator

T = TypeVar("T", bound=BaseModel)


class DeferredModel(Generic[T]):
    """https://github.com/pydantic/pydantic/issues/559#issuecomment-519686409"""

    def __init__(self, type_: Type[T], kwargs: dict[str, Any]):
        self.type_ = type_
        self.kwargs = kwargs

    def validate(self) -> T:
        return self.type_(**self.kwargs)

    def __repr__(self):
        return f"{type(self).__name__}(type_={self.type_.__name__}, kwargs={self.kwargs})"


class DeferrableModel(BaseModel):
    @classmethod
    def defer(cls: Type[T], **kwargs: Any) -> DeferredModel[T]:
        return DeferredModel(cls, kwargs)


def str_not_empty(value: str) -> str:
    """Prevents empty strings from being valid when requiring a string input."""
    if value == "":
        raise ValueError(f"'{value}' must not be empty.")
    return value


class StoryStructure(BaseModel):
    """
    Parent to all the story structure types.
    """

    # Todo: Identify a way to generate a list of types of the classes that subclass StoryStructure to
    #  dynamically update the StoryStructureData.structure property. If possible.++
    ...


class ClassicStoryStructure(StoryStructure):
    exposition: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class ThreeActStructure(StoryStructure):
    act_1_exposition: str
    act_1_inciting_incident: str
    act_1_plot_point_1: str
    act_2_rising_action: str
    act_2_midpoint: str
    act_2_plot_point_2: str
    act_3_pre_climax: str
    act_3_climax: str
    act_3_denouement: str


class FiveActStructure(StoryStructure):
    exposition: str
    rising_action: str
    climax: str
    falling_action: str
    resolution: str


class SevenPointStoryStructure(StoryStructure):
    hook: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_1: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_1: Annotated[str, AfterValidator(str_not_empty)]
    mid_point: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_2: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_2: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class FreytagsPyramidStoryStructure(StoryStructure):
    exposition: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    denouement: Annotated[str, AfterValidator(str_not_empty)]


class TheHerosJourneyStoryStructure(StoryStructure):
    the_ordinary_world: Annotated[str, AfterValidator(str_not_empty)]
    the_call_to_adventure: Annotated[str, AfterValidator(str_not_empty)]
    the_refusal_of_the_call: Annotated[str, AfterValidator(str_not_empty)]
    meeting_the_mentor: Annotated[str, AfterValidator(str_not_empty)]
    crossing_the_threshold: Annotated[str, AfterValidator(str_not_empty)]
    tests_allies_enemies: Annotated[str, AfterValidator(str_not_empty)]
    approach_to_the_inmost_cave: Annotated[str, AfterValidator(str_not_empty)]
    the_ordeal: Annotated[str, AfterValidator(str_not_empty)]
    seizing_the_sword: Annotated[str, AfterValidator(str_not_empty)]
    the_road_back: Annotated[str, AfterValidator(str_not_empty)]
    resurrection: Annotated[str, AfterValidator(str_not_empty)]
    return_with_the_elixir: Annotated[str, AfterValidator(str_not_empty)]


class DanHarmonsStoryCircleStructure(StoryStructure):
    you: Annotated[str, AfterValidator(str_not_empty)]
    need: Annotated[str, AfterValidator(str_not_empty)]
    go: Annotated[str, AfterValidator(str_not_empty)]
    search: Annotated[str, AfterValidator(str_not_empty)]
    find: Annotated[str, AfterValidator(str_not_empty)]
    take: Annotated[str, AfterValidator(str_not_empty)]
    returns: Annotated[str, AfterValidator(str_not_empty)]  # Normally "return" but it clashes with python's return.
    change: Annotated[str, AfterValidator(str_not_empty)]


class StorySpine(StoryStructure):
    once_upon_a_time: Annotated[str, AfterValidator(str_not_empty)]
    and_every_day: Annotated[str, AfterValidator(str_not_empty)]
    until_one_day: Annotated[str, AfterValidator(str_not_empty)]
    and_because_of_this: Annotated[str, AfterValidator(str_not_empty)]
    and_then: Annotated[str, AfterValidator(str_not_empty)]
    until_finally: Annotated[str, AfterValidator(str_not_empty)]
    and_ever_since_that_day: Annotated[str, AfterValidator(str_not_empty)]


class FichteanCurveStructure(StoryStructure):
    inciting_incident: Annotated[str, AfterValidator(str_not_empty)]
    first_crisis: Annotated[str, AfterValidator(str_not_empty)]
    second_crisis: Annotated[str, AfterValidator(str_not_empty)]
    third_crisis: Annotated[str, AfterValidator(str_not_empty)]
    fourth_crisis: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]


class InMediasRes(StoryStructure):
    in_medias_res: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    explanation: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class SaveTheCatStructure(StoryStructure):
    opening_image: Annotated[str, AfterValidator(str_not_empty)]
    set_up: Annotated[str, AfterValidator(str_not_empty)]
    theme_stated: Annotated[str, AfterValidator(str_not_empty)]
    catalyst: Annotated[str, AfterValidator(str_not_empty)]
    debate: Annotated[str, AfterValidator(str_not_empty)]
    break_into_two: Annotated[str, AfterValidator(str_not_empty)]
    b_story: Annotated[str, AfterValidator(str_not_empty)]
    fun_and_games: Annotated[str, AfterValidator(str_not_empty)]
    midpoint: Annotated[str, AfterValidator(str_not_empty)]
    bad_guys_close_in: Annotated[str, AfterValidator(str_not_empty)]
    all_is_lost: Annotated[str, AfterValidator(str_not_empty)]
    dark_night_of_the_soul: Annotated[str, AfterValidator(str_not_empty)]
    break_into_three: Annotated[str, AfterValidator(str_not_empty)]
    finale: Annotated[str, AfterValidator(str_not_empty)]
    final_image: Annotated[str, AfterValidator(str_not_empty)]


# End of the Story Structure section


class GeneralData(BaseModel):
    """
    A model to represent the general details of a story as defined by the structured output of an LLM.
    This model must match the json schema of the LLM's response_format input.
    """

    title: Annotated[str, AfterValidator(str_not_empty)]
    themes: list[Annotated[str, AfterValidator(str_not_empty)]]
    genres: list[Annotated[str, AfterValidator(str_not_empty)]]
    synopsis: Annotated[str, AfterValidator(str_not_empty)]

    @field_validator("title")
    @classmethod
    def clean_title(cls, value):
        value.strip()
        if ":" in value:
            """Windows directories cannot contain colons (:)."""
            value = re.sub(":", " -", value)
        return value

    @field_validator("themes", "genres")
    @classmethod
    def clean_arrays(cls, value):
        """
        Account for some of the weird ways the LLM outputs sometimes.

        Examples: ["Self-discovery | Friendship | Redemption"]
        """
        for item in value:
            if "|" in item:
                sub_values = item.split("|")
                value.remove(item)
                value.extend(sub_values)

        # Clean up any whitespace.
        for item in value:
            item.strip()

        return value


class StoryStructureData(BaseModel):
    style: str  # e.g. "Three-Act Structure"
    structure: Union[
        ClassicStoryStructure,
        ThreeActStructure,
        FiveActStructure,
        SevenPointStoryStructure,
        FreytagsPyramidStoryStructure,
        TheHerosJourneyStoryStructure,
        DanHarmonsStoryCircleStructure,
        StorySpine,
        FichteanCurveStructure,
        InMediasRes,
        SaveTheCatStructure,
    ]


class CharacterData(BaseModel):
    name: Annotated[str, AfterValidator(str_not_empty)]
    age: Annotated[str, AfterValidator(str_not_empty)]
    role: Annotated[str, AfterValidator(str_not_empty)]
    description: Annotated[str, AfterValidator(str_not_empty)]
    personality: Annotated[str, AfterValidator(str_not_empty)]


class ChapterCharacterData(BaseModel):
    name: Annotated[str, AfterValidator(str_not_empty)]
    status: Annotated[str, AfterValidator(str_not_empty)]


class SceneData(BaseModel):
    summary: Annotated[str, AfterValidator(str_not_empty)]
    number: int | None = None  # This is added manually. LLMs don't always count in order.
    characters: list[ChapterCharacterData]
    location: Annotated[str, AfterValidator(str_not_empty)]
    story_beats: list[Annotated[str, AfterValidator(str_not_empty)]]


class ChapterData(BaseModel):
    title: Annotated[str, AfterValidator(str_not_empty)]
    number: int | None = None  # This is added manually. LLMs don't always count in order.
    story_structure_point: Annotated[str, AfterValidator(str_not_empty)]
    location: Annotated[str, AfterValidator(str_not_empty)]
    characters: list[ChapterCharacterData]
    synopsis: Annotated[str, AfterValidator(str_not_empty)]
    scenes: list[SceneData] = []


class StoryData(BaseModel):
    general: GeneralData | None = None
    structure: StoryStructureData | None = None
    characters: list[CharacterData] | None = None
    locations: list[str] | None = None
    chapters: list[ChapterData] | None = None
