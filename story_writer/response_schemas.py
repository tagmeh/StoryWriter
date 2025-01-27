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
                "genres": {"type": "array", "items": {"type": "string"}},
                "themes": {"type": "array", "items": {"type": "string"}},
                "synopsis": {
                    "type": "string",
                },
            },
            "required": ["title", "genres", "themes", "synopsis"],
        },
        "required": ["output"],
    },
}

# Describes a response that matches the given story structure schema.
story_structure_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "output",
        "strict": "true",
        "schema": None,  # This is overwritten by the specific story structure schema.
        "required": ["output"],
    },
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
                    "name": {"type": "string"},
                    "age": {
                        "description": "Integer or more generic description.",
                        "type": "string",
                    },
                    "role": {"type": "string"},
                    "description": {"type": "string"},
                    "personality": {"type": "string"},
                },
                "required": ["name", "age", "role", "description", "personality"],
            },
        },
        "required": ["output"],
    },
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
                    "name": {"type": "string"},
                    "events": {
                        "type": "array",
                        "description": "Events that happen in this location",
                        "items": {"type": "string"},
                    },
                },
                "required": ["name", "events"],
            },
        },
        "required": ["output"],
    },
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
                    "title": {"type": "string"},
                    "story_structure_point": {
                        "description": "The relevant story structure point for this chapter.",
                        "type": "string",
                    },
                    "location": {"type": "string"},
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
                                    "type": "string",
                                },
                            },
                            "required": ["name", "status"],
                        },
                    },
                    "synopsis": {"type": "string"},
                },
                "required": [
                    "title",
                    "story_structure_point",
                    "location",
                    "characters",
                    "synopsis",
                ],
            },
        },
        "required": ["output"],
    },
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
                    "summary": {
                        "description": "Short summary of the scene.",
                        "type": "string",
                    },
                    "characters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "status": {"type": "string"},
                            },
                            "required": ["name", "status"],
                        },
                    },
                    "location": {
                        "description": "The location that this scene takes place in.",
                        "type": "string",
                    },
                    "story_beats": {
                        "description": "A few sentences of what happens in this scene.",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "title",
                    "characters",
                    "location",
                    "story_beats",
                ],
            },
        },
        "required": ["output"],
    },
}

# Story Structure Response Schemas
classic = {
    "type": "object",
    "description": "A generic story structure for all types of stories.",
    "properties": {
        "exposition": {"type": "string"},
        "rising_action": {"type": "string"},
        "climax": {"type": "string"},
        "falling_action": {"type": "string"},
        "resolution": {"type": "string"},
    },
    "required": [
        "exposition",
        "rising_action",
        "climax",
        "falling_action",
        "resolution",
    ],
}

three_act_structure = {
    "type": "object",
    "description": "Traditional story structure, most structures follow a variation on this one. Very popular in movies",
    "properties": {
        "act_1_exposition": {
            "description": "Establish the status quo.",
            "type": "string",
        },
        "act_1_inciting_incident": {
            "description": "Event that starts the story.",
            "type": "string",
        },
        "act_1_plot_point_1": {
            "description": "Protagonist has decided to deal with the conflict.",
            "type": "string",
        },
        "act_2_rising_action": {
            "description": "The hero is beset with various challenges that increase the stakes in the tension.",
            "type": "string",
        },
        "act_2_midpoint": {
            "description": "An event that turns everything on its head, nearly ruining the protagonist's chances of achieving their goal.",
            "type": "string",
        },
        "act_2_plot_point_2": {
            "description": "Following the midpoint, the protagonist fails at a challenge. Protagonist may question capability of succeeding.",
            "type": "string",
        },
        "act_3_pre_climax": {
            "description": "Protagonist pulls themself together and prepares for the final confrontation.",
            "type": "string",
        },
        "act_3_climax": {
            "description": "The final confrontation between the protagonist and antagonist. Protagonist usually wins.",
            "type": "string",
        },
        "act_3_denouement": {
            "description": "All loose ends are neatly tied up, consequences of the climax are clearly spelled out.",
            "type": "string",
        },
    },
    "required": [
        "act_1_exposition",
        "act_1_inciting_incident",
        "act_1_plot_point_1",
        "act_2_rising_action",
        "act_2_midpoint",
        "act_2_plot_point_2",
        "act_3_pre_climax",
        "act_3_climax",
        "act_3_denouement",
    ],
}

five_act_structure = {
    "type": "object",
    "description": "Basically the same as Freytag's Pyramid, but without the expectation of it being a tragedy.",
    "properties": {
        "exposition": {
            "description": "Establish the status quo. Ends with the inciting incident.",
            "type": "string",
        },
        "rising_action": {
            "description": "Protagonist pursues their goal as the stakes rise.",
            "type": "string",
        },
        "climax": {
            "description": "Center of the story, the point of no return.",
            "type": "string",
        },
        "falling_action": {
            "description": "We see the consequences of the climax. In a tragedy, things start to spiral out of control.",
            "type": "string",
        },
        "resolution": {
            "description": "Everything is wrapped up. The protagonist is usually at their highest point.",
            "type": "string",
        },
    },
    "required": [
        "exposition",
        "rising_action",
        "climax",
        "falling_action",
        "resolution",
    ],
}

seven_point_story_structure = {
    "type": "object",
    "properties": {
        "hook": {"type": "string"},
        "plot_turn_1": {"type": "string"},
        "pinch_point_1": {"type": "string"},
        "mid_point": {"type": "string"},
        "pinch_point_2": {"type": "string"},
        "plot_turn_2": {"type": "string"},
        "resolution": {"type": "string"},
    },
    "required": [
        "hook",
        "plot_turn_1",
        "pinch_point_1",
        "mid_point",
        "pinch_point_2",
        "plot_turn_2",
        "resolution",
    ],
}

freytags_pyramid = {
    "type": "object",
    "description": "A story structure for tragic narratives.",
    "properties": {
        "exposition": {
            "description": "Establish the status quo. Ends with the inciting incident.",
            "type": "string",
        },
        "rising_action": {
            "description": "Protagonist pursues their goal as the stakes rise.",
            "type": "string",
        },
        "climax": {
            "description": "Center of the story, the point of no return.",
            "type": "string",
        },
        "falling_action": {
            "description": "We see the consequences of the climax. In a tragedy, things start to spiral out of control.",
            "type": "string",
        },
        "catastrophe": {
            "description": "Everything is wrapped up. In a tragedy, the protagonist is at their lowest point.",
            "type": "string",
        },
    },
    "required": [
        "exposition",
        "rising_action",
        "climax",
        "falling_action",
        "catastrophe",
    ],
}

the_heros_journey = {
    "type": "object",
    "description": "Campbell’s original structure uses terminology that lends itself well to epic tales of bravery and triumph.",
    "properties": {
        "the_ordinary_world": {
            "description": "The hero’s everyday life is established.",
            "type": "string",
        },
        "the_call_of_adventure": {
            "description": "Otherwise known as the inciting incident.",
            "type": "string",
        },
        "refusal_of_the_call": {
            "description": "For a moment, the hero is reluctant to take on the challenge.",
            "type": "string",
        },
        "meeting_the_mentor": {
            "description": "Our hero meets someone who prepares them for what lies ahead.",
            "type": "string",
        },
        "crossing_the_threshold": {
            "description": "The hero steps out of their comfort zone and enters a ‘new world.’",
            "type": "string",
        },
        "tests_allies_enemies": {
            "description": "Our protagonist faces new challenges, and maybe picks up some new friends.",
            "type": "string",
        },
        "approach_to_the_inmost_cave": {
            "description": "The hero gets close to their goal.",
            "type": "string",
        },
        "the_ordeal": {
            "description": "The hero meets (and overcomes) their greatest challenge yet.",
            "type": "string",
        },
        "seizing_the_sword": {
            "description": "The hero obtains something important they were after, and victory is in sight.",
            "type": "string",
        },
        "the_road_back": {
            "description": "The hero realizes that achieving their goal is not the final hurdle.",
            "type": "string",
        },
        "resurrection": {
            "description": "The hero faces their final challenge — a climactic test that hinges on everything they’ve learned over their journey.",
            "type": "string",
        },
        "return_with_the_elixir": {
            "description": "Having triumphed, our protagonist returns to their old life. ",
            "type": "string",
        },
    },
    "required": [
        "the_ordinary_world",
        "the_call_of_adventure",
        "refusal_of_the_call",
        "meeting_the_mentor",
        "crossing_the_first_threshold",
        "tests_allies_enemies",
        "approach_to_the_inmost_cave",
        "the_ordeal",
        "seizing_the_sword",
        "the_road_back",
        "resurrection",
        "return_with_the_elixir",
    ],
}

dan_harmons_story_circle = {
    "type": "object",
    "description": "A hero's journey type narrative that focuses more on character development.",
    "properties": {
        "you": {"description": "", "type": "string"},
        "need": {"description": "", "type": "string"},
        "go": {"description": "", "type": "string"},
        "search": {"description": "", "type": "string"},
        "find": {"description": "", "type": "string"},
        "take": {"description": "", "type": "string"},
        "return": {"description": "", "type": "string"},
        "change": {"description": "", "type": "string"},
    },
    "required": ["you", "need", "go", "search", "find", "take", "_return", "change"],
}

story_spine = {
    "type": "object",
    "description": "",
    "properties": {
        "once_upon_a_time": {
            "description": "Setup protagonist and the starting situation.",
            "type": "string",
        },
        "and_every_day": {
            "description": "More exposition, describing the status quo.",
            "type": "string",
        },
        "until_one_day": {
            "description": "Inciting incident to shake things up.",
            "type": "string",
        },
        "and_because_of_this": {
            "description": "Protagonists are forced to leave their normal lives and go on an adventure.",
            "type": "string",
        },
        "and_then": {
            "description": "The pursuit of their goals have consequences. A goal may have been achieved, but it leads to something else.",
            "type": "string",
        },
        "until_finally": {"description": "Climax of the story.", "type": "string"},
        "and_ever_since_that_day": {
            "description": "How did the hero change from the journey. What did they bring back with them.",
            "type": "string",
        },
    },
    "required": [
        "once_upon_a_time",
        "and_every_day",
        "until_one_day",
        "and_because_of_this",
        "and_then",
        "until_finally",
        "and_ever_since_that_day",
    ],
}

fichtean_curve = {
    "type": "object",
    "description": "Packed with tension and mini-crises, the protagonist goes through multiple obstacles along their journey. Bypasses the 'ordinary world' setup.",
    "properties": {
        "inciting_incident": {"description": "", "type": "string"},
        "first_crisis": {"description": "", "type": "string"},
        "second_crisis": {"description": "", "type": "string"},
        "third_crisis": {"description": "", "type": "string"},
        "fourth_crisis": {"description": "", "type": "string"},
        "climax": {"description": "", "type": "string"},
        "falling_action": {"description": "", "type": "string"},
    },
    "required": [
        "inciting_incident",
        "first_crisis",
        "second_crisis",
        "third_crisis",
        "fourth_crisis",
        "climax",
        "falling_action",
    ],
}

in_medias_res = {
    "type": "object",
    "description": "Framework for starting the story in the middle of the action.",
    "properties": {
        "in_medias_res": {
            "description": "Starts off immediately in the action with little to no exposition or backstory.",
            "type": "string",
        },
        "rising_action": {
            "description": "Conflict increases, characters have to adjust. Still don't know everything going on at this time.",
            "type": "string",
        },
        "explanation": {
            "description": "Rest point where exposition or backstory informs the reader what or why things are happening.",
            "type": "string",
        },
        "climax": {
            "description": "Everything comes together and the protagonist succeeds or fails.",
            "type": "string",
        },
        "falling_action": {
            "description": "All loose ends are tied up and the reader is allowed to breathe.",
            "type": "string",
        },
        "resolution": {
            "description": "Protagonist returns to their ordinary world and plot threads are addressed.",
            "type": "string",
        },
    },
    "required": [
        "in_medias_res",
        "rising_action",
        "explanation",
        "climax",
        "falling_action",
        "resolution",
    ],
}

save_the_cat = {
    "type": "object",
    "description": "A more detailed version of the three act structure.",
    "properties": {
        "opening_image": {
            "description": "Story starts out with a brief look at the protagonist, gets the feel and tone of the story.",
            "type": "string",
        },
        "set_up": {
            "description": "A little more exposition, setup the tone of the world, introduce the characters.",
            "type": "string",
        },
        "theme_stated": {
            "description": "Make clear what the theme is. The theme may becomes more obvious to the progatonist as the story progresses.",
            "type": "string",
        },
        "catalyst": {
            "description": "The inciting incident. The journey begins.",
            "type": "string",
        },
        "debate": {
            "description": "Protagonist fights or debates with the path they have taken.",
            "type": "string",
        },
        "break_into_two": {
            "description": "Protagonist is fully invested in their quest.",
            "type": "string",
        },
        "b_story": {
            "description": "Introduced to the b plot of the story.",
            "type": "string",
        },
        "fun_and_games": {
            "description": "Protagonist enjoys a small amount of time to enjoy their new life, world, and abilities they have gained.",
            "type": "string",
        },
        "midpoint": {
            "description": "Something happens to turn the everything on its head.",
            "type": "string",
        },
        "bad_guys_close_in": {
            "description": "The antagonist's forces become a greater threat to the protagonist.",
            "type": "string",
        },
        "all_is_lost": {
            "description": "Something happens to the protagonist and puts them under extreme duress. ",
            "type": "string",
        },
        "dark_night_of_the_soul": {
            "description": "The protagonist goes through a depressive period when it seems all hope is lost.",
            "type": "string",
        },
        "break_into_three": {
            "description": "Protagonist rises up from rock bottom and gains a key piece of knowledge that helps them in the future.",
            "type": "string",
        },
        "finale": {
            "description": "Protagonist takes what they have learned from their journey to defeat the antagonist.",
            "type": "string",
        },
        "final_image": {
            "description": "The final snapshot of the story, it should mirror the opening image.",
            "type": "string",
        },
    },
    "required": [
        "opening_image",
        "set_up",
        "theme_stated",
        "catalyst",
        "debate",
        "break_into_two",
        "b_story",
        "fun_and_games",
        "midpoint",
        "bad_guys_close_in",
        "all_is_lost",
        "dark_night_of_the_soul",
        "break_into_three",
        "finale",
        "final_image",
    ],
}
