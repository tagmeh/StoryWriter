from enum import Enum
from typing import Type

from pydantic import BaseModel

from story_writer import response_schemas
from story_writer import story_data_model


class StoryStructure(Enum):
    CLASSIC = "Classic"
    SEVEN_POINT = "Seven Point Story Structure"
    FREYTAGS_PYRAMID = "Freytag's Pyramid"
    THE_HEROS_JOURNEY = "The Hero's Journey"
    DAN_HARMONS_STORY_CIRCLE = "Dan Harmon's Story Circle"
    FICHTEAN_CURVE = "Fichtean Curve"
    SAVE_THE_CAT = "Save the Cat Beat Sheet"


def get_story_structure_schema(story_structure: StoryStructure) -> dict:
    print(f'Story Structure: {story_structure.value}')
    schemas = {
        StoryStructure.SEVEN_POINT: response_schemas.seven_point_story_structure,
        StoryStructure.CLASSIC: response_schemas.classic,
        StoryStructure.FREYTAGS_PYRAMID: response_schemas.freytags_pyramid,
        StoryStructure.THE_HEROS_JOURNEY: response_schemas.the_heros_journey,
        StoryStructure.DAN_HARMONS_STORY_CIRCLE: response_schemas.dan_harmons_story_circle,
        StoryStructure.FICHTEAN_CURVE: response_schemas.fichtean_curve,
        StoryStructure.SAVE_THE_CAT: response_schemas.save_the_cat,
    }
    return schemas.get(story_structure, response_schemas.classic)


def get_story_structure_model(story_structure: StoryStructure) -> Type[BaseModel]:
    models = {
        StoryStructure.SEVEN_POINT: story_data_model.SevenPointStoryStructure,
        StoryStructure.CLASSIC: story_data_model.ClassicStoryStructure,
        # StoryStructure.FREYTAGS_PYRAMID: story_data_model.FreytagsPyramidData,
        # StoryStructure.THE_HEROS_JOURNEY: story_data_model.TheHerosJourneyData,
        # StoryStructure.DAN_HARMONS_STORY_CIRCLE: story_data_model.DanHarmonsStoryCircleData,
        # StoryStructure.FICHTEAN_CURVE: story_data_model.FichteanCurveData,
        # StoryStructure.SAVE_THE_CAT: story_data_model.SaveTheCatData,
    }
    return models.get(story_structure, story_data_model.ClassicStoryStructure)
