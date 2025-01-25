from enum import Enum


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
        StoryStructure.SEVEN_POINT: seven_point_story_structure,
        StoryStructure.CLASSIC: classic,
        StoryStructure.FREYTAGS_PYRAMID: freytags_pyramid,
        StoryStructure.THE_HEROS_JOURNEY: the_heros_journey,
        StoryStructure.DAN_HARMONS_STORY_CIRCLE: None,
        StoryStructure.FICHTEAN_CURVE: None,
        StoryStructure.SAVE_THE_CAT: None,
    }
    return schemas.get(story_structure, classic)


classic = {
    "type": "object",
    "description": "A generic story structure for all types of stories.",
    "properties": {
        "exposition": {
            "type": "string"
        },
        "rising action": {
            "type": "string"
        },
        "climax": {
            "type": "string"
        },
        "falling action": {
            "type": "string"
        },
        "resolution": {
            "type": "string"
        },
    },
    "required": ["exposition", "rising action", "climax", "falling action", "resolution"]
}

seven_point_story_structure = {
    "type": "object",
    "properties": {
        "hook": {
            "type": "string"
        },
        "plot point 1": {
            "type": "string"
        },
        "pinch point 1": {
            "type": "string"
        },
        "mid point": {
            "type": "string"
        },
        "pinch point 2": {
            "type": "string"
        },
        "plot point 2": {
            "type": "string"
        },
        "resolution": {
            "type": "string"
        }
    },
    "required": ["hook", "plot point 1", "pinch point 1", "mid point", "pinch point 2",
                 "plot point 2", "resolution"]
}

freytags_pyramid = {
    "type": "object",
    "description": "A story structure for tragic narratives.",
    "properties": {
        "introduction": {
            "type": "string"
        },
        "rising action": {
            "type": "string"
        },
        "climax": {
            "type": "string"
        },
        "falling action": {
            "type": "string"
        },
        "catastrophe": {
            "type": "string"
        },
    },
    "required": ["exposition", "rising action", "climax", "falling action", "catastrophe"]
}

the_heros_journey = {
    "type": "object",
    "description": "Campbell’s original structure uses terminology that lends itself well to epic tales of bravery and triumph.",
    "properties": {
        "the ordinary world": {
            "description": "The hero’s everyday life is established.",
            "type": "string"
        },
        "the call of adventure": {
            "description": "Otherwise known as the inciting incident.",
            "type": "string"
        },
        "refusal of the call": {
            "description": "For a moment, the hero is reluctant to take on the challenge.",
            "type": "string"
        },
        "meeting the mentor": {
            "description": "Our hero meets someone who prepares them for what lies ahead.",
            "type": "string"
        },
        "crossing the first threshold": {
            "description": "The hero steps out of their comfort zone and enters a ‘new world.’",
            "type": "string"
        },
        "tests allies enemies": {
            "description": "Our protagonist faces new challenges, and maybe picks up some new friends.",
            "type": "string"
        },
        "approach to the inmost cave": {
            "description": "The hero gets close to their goal.",
            "type": "string"
        },
        "the ordeal": {
            "description": "The hero meets (and overcomes) their greatest challenge yet.",
            "type": "string"
        },
        "seizing the sword": {
            "description": "The hero obtains something important they were after, and victory is in sight.",
            "type": "string"
        },
        "the road back": {
            "description": "The hero realizes that achieving their goal is not the final hurdle.",
            "type": "string"
        },
        "resurrection": {
            "description": "The hero faces their final challenge — a climactic test that hinges on everything they’ve learned over their journey.",
            "type": "string"
        },
        "return with the elixir": {
            "description": "Having triumphed, our protagonist returns to their old life. ",
            "type": "string"
        }
    },
    "required": ["the ordinary world", "the call of adventure", "refusal of the call", "meeting the mentor",
                 "crossing the first threshold", "tests allies enemies", "approach to the inmost cave", "the ordeal",
                 "seizing the sword", "the road back", "resurrection", "return with the elixir", ]
}

dan_harmons_story_circle = {}

fichtean_curve = {}

save_the_cat = {}