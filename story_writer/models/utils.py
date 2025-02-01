import logging
from typing import Any

from pydantic import BaseModel, TypeAdapter

from story_writer.constants import StoryStructureEnum
from story_writer.models.outline_models.story_structure_models import (
    ClassicStoryStructure,
    DanHarmonsStoryCircleStructure,
    FichteanCurveStructure,
    FiveActStructure,
    FreytagsPyramidStoryStructure,
    InMediasRes,
    SaveTheCatStructure,
    SevenPointStoryStructure,
    StorySpine,
    TheHerosJourneyStoryStructure,
    ThreeActStructure,
)

log = logging.getLogger(__name__)


STORY_STYLE_MODEL_MAPPING = {
    StoryStructureEnum.CLASSIC_STORY_STRUCTURE: ClassicStoryStructure,
    StoryStructureEnum.THREE_ACT_STRUCTURE: ThreeActStructure,
    StoryStructureEnum.FIVE_ACT_STRUCTURE: FiveActStructure,
    StoryStructureEnum.SEVEN_POINT_STORY_STRUCTURE: SevenPointStoryStructure,
    StoryStructureEnum.FREYTAGS_PYRAMID: FreytagsPyramidStoryStructure,
    StoryStructureEnum.THE_HEROS_JOURNEY: TheHerosJourneyStoryStructure,
    StoryStructureEnum.DAN_HARMONS_STORY_CIRCLE: DanHarmonsStoryCircleStructure,
    StoryStructureEnum.STORY_SPINE: StorySpine,
    StoryStructureEnum.FICHTEAN_CURVE: FichteanCurveStructure,
    StoryStructureEnum.IN_MEDIAS_RES: InMediasRes,
    StoryStructureEnum.SAVE_THE_CAT: SaveTheCatStructure,
}


def create_json_schema(model: type[BaseModel]) -> dict[str, Any] | None:
    array_models = ["CharacterData", "ChapterData", "SceneData"]
    if model.__name__ in array_models:
        schema = TypeAdapter(list[model]).json_schema()
    else:
        schema = model.model_json_schema()
    return (
        {
            "type": "json_schema",
            "json_schema": {"name": model.__name__, "strict": True, "schema": schema, "required": [model.__name__]},
        }
        if schema
        else None
    )
