from enum import Enum


class StoryStructureEnum(Enum):
    CLASSIC_STORY_STRUCTURE = "Classic Story Structure"
    THREE_ACT_STRUCTURE = "Three Act Structure"
    FIVE_ACT_STRUCTURE = "Five Act Structure"
    SEVEN_POINT_STORY_STRUCTURE = "Seven Point Story Structure"
    FREYTAGS_PYRAMID = "Freytag's Pyramid"
    THE_HEROS_JOURNEY = "The Hero's Journey"
    DAN_HARMONS_STORY_CIRCLE = "Dan Harmon's Story Circle"
    STORY_SPINE = "Story Spine"
    FICHTEAN_CURVE = "Fichtean Curve"
    IN_MEDIAS_RES = "In Medias Res"
    SAVE_THE_CAT = "Save the Cat"

    @classmethod
    def _missing_(cls, value: str) -> "StoryStructureEnum":
        """Accepts a string and attempts to return the matching StoryStructureEnum object."""

        def clean(val: str) -> str:
            return val.strip().lower().replace("'", "").replace(" ", "")

        normalized_value = clean(value)
        for val in StoryStructureEnum:
            if clean(val.value) == normalized_value:
                return val
        raise ValueError(
            f"'{value}' is not a supported Story Structure Type. Use one of: {', '.join([ss.value for ss in StoryStructureEnum])}"
        )


class StorySaveFormatEnum(Enum):
    JSON = "json"
    YAML = "yaml"

    @classmethod
    def _missing_(cls, value: str) -> "StorySaveFormatEnum":
        """Accepts a string and attempts to return the matching StorySaveFormatEnum object."""
        normalized_value = value.strip().lower()
        for val in StorySaveFormatEnum:
            if val.value.strip().lower() == normalized_value:
                return val
        raise ValueError(
            f"'{value}' is not a supported Save Format. Use one of: {', '.join([ss.value for ss in StorySaveFormatEnum])}"
        )
