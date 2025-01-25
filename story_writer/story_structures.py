from enum import Enum
import response_schemas


class StoryStructure(Enum):
    SEVEN_POINT = "Seven Point Story Structure"
    CLASSIC = "Classic"
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
