from enum import Enum


class StoryStructureEnum(Enum):
    CLASSIC = "Classic Story Structure"
    THREE_ACT_STRUCTURE = "Three Act Structure"
    FIVE_ACT_STRUCTURE = "Five Act Structure"
    SEVEN_POINT = "Seven Point Story Structure"
    FREYTAGS_PYRAMID = "Freytag's Pyramid"
    THE_HEROS_JOURNEY = "The Hero's Journey"
    DAN_HARMONS_STORY_CIRCLE = "Dan Harmon's Story Circle"
    STORY_SPINE = "Story Spine"
    FICHTEAN_CURVE = "Fichtean Curve"
    IN_MEDIAS_RES = "In Medias Res"
    SAVE_THE_CAT = "Save the Cat"


class StorySaveFormatEnum(Enum):
    JSON = "json"
    YAML = "yaml"
