# Story Step Response Schemas

# Describes a response with a "title", "genres", "themes", and "synopsis" for a story.
story_general_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                },
                "genres": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "themes": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "synopsis": {
                    "type": "string",
                },
            },
            "required": [
                "title",
                "genres",
                "themes",
                "synopsis"
            ]
        },
        "required": ["output"]
    }
}

# Describes a response that matches the given story structure schema.
story_structure_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": None,  # This is overwritten by the specific story structure schema.
        "required": ["output"]
    }
}

# Describes a response with an array of characters, each with
#  a "name", "age", "reason in story", "description", and "personality".
story_characters_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "age": {
                        "description": "Integer or more generic description.",
                        "type": "string"
                    },
                    "reason in story": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "personality": {
                        "type": "string"
                    }
                },
                "required": [
                    "name",
                    "age",
                    "reason in story",
                    "description",
                    "personality"
                ]
            }
        },
        "required": ["output"]
    }
}

# Describes a response with an array of locations, each with
#  a "name" and "events" that happen in that location.
story_locations_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "events": {
                        "type": "array",
                        "description": "Events that happen in this location",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["name", "events"]
            }
        },
        "required": ["output"]
    }
}

# Describes a response with an array of chapters, each with
#  a "title", "chapter number", "story structure point", "location", "characters", and "synopsis".
story_chapters_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "chapter number": {
                        "type": "integer"
                    },
                    "story structure point": {
                        "description": "The relevant story structure point for this chapter.",
                        "type": "string"
                    },
                    "location": {
                        "type": "string"
                    },
                    "characters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                },
                                "status": {
                                    "description": "Alive, dead, missing, transformed, dazed, asleep, etc",
                                    "type": "string"
                                }
                            },
                            "required": ["name", "status"]
                        }
                    },
                    "synopsis": {
                        "type": "string"
                    }
                },
                "required": [
                    "title",
                    "chapter number",
                    "story structure point",
                    "location",
                    "characters",
                    "synopsis"
                ]
            }
        },
        "required": ["output"]
    }
}

# Describes a response with an array of scenes for a chapter, each with
#  a "scene number", "characters", "location", and "story beats".
#  (Associated chapter number is attached after generation)
story_chapter_scene_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene number": {
                        "type": "integer"
                    },
                    "characters": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "location": {
                        "description": "The location that this scene takes place in.",
                        "type": "string"
                    },
                    "story beats": {
                        "description": "A few sentences of what happens in this scene.",
                        "type": "string"
                    }
                },
                "required": ["scene number", "characters", "location", "story beats"]
            }
        },
        "required": ["output"]
    }
}

# Story Structure Response Schemas
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
