from enum import Enum

from story_writer import story_data_model as model


class StoryStructureEnum(Enum):
    CLASSIC = model.ClassicStoryStructure
    THREE_ACT_STRUCTURE = model.ThreeActStructure
    FIVE_ACT_STRUCTURE = model.FiveActStructure
    SEVEN_POINT = model.SevenPointStoryStructure
    FREYTAGS_PYRAMID = model.FreytagsPyramidStoryStructure
    THE_HEROS_JOURNEY = model.TheHerosJourneyStoryStructure
    DAN_HARMONS_STORY_CIRCLE = model.DanHarmonsStoryCircleStructure
    STORY_SPINE = model.StorySpine
    FICHTEAN_CURVE = model.FichteanCurveStructure
    IN_MEDIAS_RES = model.InMediasRes
    SAVE_THE_CAT = model.SaveTheCatStructure


class StorySaveFormatEnum(Enum):
    JSON = "json"
    YAML = "yaml"
