import logging
from enum import Enum

from pydantic import BaseModel

from story_writer import response_schemas, story_data_model

log = logging.getLogger(__name__)


class StoryStructure(Enum):
    CLASSIC = "Classic"
    THREE_ACT_STRUCTURE = "Three Act Story Structure"
    FIVE_ACT_STRUCTURE = "Five Act Story Structure"
    SEVEN_POINT = "Seven Point Story Structure"
    FREYTAGS_PYRAMID = "Freytag's Pyramid"
    THE_HEROS_JOURNEY = "The Hero's Journey"
    DAN_HARMONS_STORY_CIRCLE = "Dan Harmon's Story Circle"
    STORY_SPINE = "Story Spine"
    FICHTEAN_CURVE = "Fichtean Curve"
    IN_MEDIAS_RES = "In Medias Res"
    SAVE_THE_CAT = "Save the Cat Beat Sheet"


structure_config = {
    StoryStructure.CLASSIC: {
        "schema": response_schemas.classic,
        "model": story_data_model.ClassicStoryStructure,
    },
    StoryStructure.THREE_ACT_STRUCTURE: {
        "schema": response_schemas.three_act_structure,
        "model": story_data_model.ThreeActStructure,
    },
    StoryStructure.FIVE_ACT_STRUCTURE: {
        "schema": response_schemas.five_act_structure,
        "model": story_data_model.FiveActStructure,
    },
    StoryStructure.SEVEN_POINT: {
        "schema": response_schemas.seven_point_story_structure,
        "model": story_data_model.SevenPointStoryStructure,
    },
    StoryStructure.FREYTAGS_PYRAMID: {
        "schema": response_schemas.freytags_pyramid,
        "model": story_data_model.FreytagsPyramidStoryStructure,
    },
    StoryStructure.THE_HEROS_JOURNEY: {
        "schema": response_schemas.the_heros_journey,
        "model": story_data_model.TheHerosJourneyStoryStructure,
    },
    StoryStructure.DAN_HARMONS_STORY_CIRCLE: {
        "schema": response_schemas.dan_harmons_story_circle,
        "model": story_data_model.DanHarmonsStoryCircleStructure,
    },
    StoryStructure.STORY_SPINE: {
        "schema": response_schemas.story_spine,
        "model": story_data_model.StorySpine,
    },
    StoryStructure.FICHTEAN_CURVE: {
        "schema": response_schemas.fichtean_curve,
        "model": story_data_model.FichteanCurveStructure,
    },
    StoryStructure.IN_MEDIAS_RES: {
        "schema": response_schemas.in_medias_res,
        "model": story_data_model.InMediasRes,
    },
    StoryStructure.SAVE_THE_CAT: {
        "schema": response_schemas.save_the_cat,
        "model": story_data_model.SaveTheCatStructure,
    },
}


def get_story_structure_schema(story_structure: StoryStructure) -> dict:
    try:
        log.debug(f"Story Structure: {story_structure.value}")
        return structure_config[story_structure]["schema"]
    except KeyError as err:
        raise ValueError(f"Invalid story structure: {story_structure} - Error: {err}") from err


def get_story_structure_model(story_structure: StoryStructure) -> type[BaseModel]:
    try:
        return structure_config[story_structure]["model"]
    except KeyError as err:
        raise ValueError(f"Invalid story structure: {story_structure} - Error: {err}") from err
