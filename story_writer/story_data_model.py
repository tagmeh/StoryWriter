import re
from typing import Any, TypeVar, Type, Generic

from pydantic import BaseModel, field_validator

T = TypeVar("T", bound=BaseModel)


class DeferredModel(Generic[T]):
    """ https://github.com/pydantic/pydantic/issues/559#issuecomment-519686409 """

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


class GeneralData(BaseModel):
    """
    A model to represent the general details of a story as defined by the structured output of an LLM.
    This model must match the json schema of the LLM's response_format input.
    """
    title: str
    themes: list[str]
    genres: list[str]
    synopsis: str

    @field_validator('title')
    @classmethod
    def clean_title(cls, value):
        value.strip()
        if ":" in value:
            """ Windows directories cannot contain colons (:). """
            value = re.sub(":", " -", value)
        return value

    @field_validator('themes', 'genres')
    @classmethod
    def clean_themes(cls, value):
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


class StoryStructureOptions(BaseModel):
    ...


class ClassicStoryStructure(StoryStructureOptions):
    exposition: str
    rising_action: str
    climax: str
    falling_action: str
    resolution: str


class SevenPointStoryStructure(StoryStructureOptions):
    hook: str
    plot_turn_1: str
    pinch_point_1: str
    mid_point: str
    pinch_point_2: str
    plot_turn_2: str
    resolution: str


class FreytagsPyramidStoryStructure(StoryStructureOptions):
    exposition: str
    rising_action: str
    climax: str
    falling_action: str
    denouement: str


class TheHerosJourneyStoryStructure(StoryStructureOptions):
    the_ordinary_world: str
    the_call_to_adventure: str
    the_refusal_of_the_call: str
    meeting_the_mentor: str
    crossing_the_threshold: str
    tests_allies_enemies: str
    approach_to_the_inmost_cave: str
    the_ordeal: str
    seizing_the_sword: str
    the_road_back: str
    resurrection: str
    return_with_the_elixir: str


class DanHarmonsStoryCircleStructure(StoryStructureOptions):
    ...


class FichteanCurveStructure(StoryStructureOptions):
    ...


class SaveTheCatStructure(StoryStructureOptions):
    ...


class StoryStructureData(BaseModel):
    style: str  # e.g. "Three-Act Structure"
    structure: StoryStructureOptions


class CharacterData(BaseModel):
    name: str
    role: str
    description: str


class SceneData(BaseModel):
    scene_number: int
    title: str
    characters: list[CharacterData]
    location: str
    story_beats: str


class ChapterData(BaseModel):
    chapter_number: int
    title: str
    story_structure_point: str
    characters: list[str]
    location: list[str]
    synopsis: str
    scenes: list[SceneData] = []


class StoryData(BaseModel):
    general: GeneralData | None = None
    structure: StoryStructureData | None = None
    characters: list[CharacterData] | None = None
    locations: list[str] | None = None
    chapters: list[ChapterData] | None = None
