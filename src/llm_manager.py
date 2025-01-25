import json
import re
import time
from json import JSONDecodeError
from pathlib import Path
from typing import Optional

import openai
import yaml

from src import utils
from src.constants.models import FIRST_PASS_GENERATION_MODEL
from src.constants.system import GENERAL_SYSTEM_PROMPT
from src.story_schemas import StoryStructure, get_story_structure_schema

story_data = {
    "general": {},
    "structure": {},
    "characters": {},
    "chapters": {}
}


def stream_llm(client, messages, model, response_format):
    start = time.time()
    max_retries = 5
    retries = 0
    while retries < max_retries:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            response_format=response_format,
            stream=True,
            stream_options={"include_usage": True}  # Doesn't work for LM Studio?
        )

        output = ""
        for chunk in response:
            if not chunk.choices[0].delta.content is None and chunk.choices[0].delta.role == "assistant":
                output += chunk.choices[0].delta.content

        elapsed = time.time() - start

        try:
            content = json.loads(output)
            from pprint import pprint
            pprint(content, sort_dicts=False)
        except JSONDecodeError as err:
            print(f'JSON Error: "{err}" Retrying...')
            retries += 1
            continue

        if content == {}:
            print(f'No content returned from LLM. "{content}')
            retries += 1

        else:
            return content, elapsed, retries

    if retries >= max_retries:
        print(f'Failed to get any data from the LLM in {retries} attempts.')


def call_llm(client, messages, model, response_format):
    start = time.time()
    max_retries = 5
    retries = 0
    while retries < max_retries:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            response_format=response_format
        )
        elapsed = time.time() - start

        try:
            content = json.loads(response.choices[0].message.content)
            from pprint import pprint
            pprint(content, sort_dicts=False)
        except JSONDecodeError as err:
            print(f'JSON Error: "{err}" Retrying...')
            retries += 1
            continue

        if content == {}:
            print(f'No content returned from LLM. "{content}')
            retries += 1

        else:
            return content, elapsed, retries

    if retries >= max_retries:
        print(f'Failed to get any data from the LLM in {retries} attempts.')


def expand_initial_prompt(client: openai.Client, user_prompt) -> Path | None:
    """
    Uses the LLM to expand and enhance the user_prompt input to create a complete story from end to end.
    Instructs the LLM to respond with a Title, Genre tags, and the Synopsis (Updated user_prompt input)

    :param client: Facilitates LLM connection and communication
    :param user_prompt: User's initial
    :return:
    """

    instructions = f"""
    Expand on the user input (below) and work out a complete story from start to finish.
    Respond with a clever title, fitting genre tags, the general themes, and the improved and expanded synopsis.
    
    User Input: {user_prompt}
    
    Respond with some title options, the genre tags, a general themes, and the synopsis.
    """

    response_format: dict = {
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
                "required": ["title", "genres", "themes", "synopsis"]
            }
        }
    }

    messages = [
        {
            "role": "system",
            "content": GENERAL_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": instructions
        }
    ]

    content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
                                           response_format=response_format)

    # TODO: Move checks/validators/cleaners to a new directory
    # Checks and cleanups?
    if ":" in content['title']:
        """ Colons (:) cannot be used to create directories in Windows. """
        content['title'] = re.sub(":", " -", content['title'])

    # TODO: Add story chapter checking? This only happens when running this section, ie. creating a new story.
    #   Solution might be to shoot off a small call to the src with the output's body as context to get only
    #   a {"title": "<title>"} back.
    project_root = Path(__file__).parents[1]  # ../StoryWriter/
    story_root = Path(f"{project_root}/stories/{content['title']}")
    story_root.mkdir(parents=True, exist_ok=True)

    story_data['general'] = content

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

    file_name = f"expand_initial_prompt-{retries}" if retries > 0 else "expand_initial_prompt"
    utils.log_step(story_root=story_root, messages=messages, file_name=file_name, model=FIRST_PASS_GENERATION_MODEL,
                   settings={}, response_format=response_format, duration=elapsed)

    return story_root


def generate_story_structure(client: openai.Client, story_root: Path, story_structure: Optional[StoryStructure] = None):
    start = time.time()

    story_structure = story_structure or StoryStructure.CLASSIC

    # Load story-specific content.
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = yaml.safe_load(f)

    if not story_data["general"]:
        raise Exception("General story details do not exist, create a new story before generating the story structure.")

    instructions = f"""
    Generate a story structure/outline using the following story structure style: {story_structure.value}.
    Expand on each point in the story, adding details where appropriate. Avoid dialogue at this stage. 
    
    Consider the protagonist's motivations and desires.
    What issues does the protagonist run into, how do they overcome them?
    Does anyone help or hinder the protagonist?
    
    User Input:
    Title: {story_data["general"]['title']}
    Genres: {story_data["general"]['genres']}
    Themes: {story_data["general"]['themes']}
    Synopsis: {story_data["general"]['synopsis']}
    """

    response_format: dict = {
        "type": "json_schema",
        "json_schema": {
            "name": "output",
            "strict": "true",
            "schema": get_story_structure_schema(story_structure)
        }
    }

    messages = [
        {
            "role": "system",
            "content": GENERAL_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": instructions
        }
    ]

    content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
                                           response_format=response_format)
    story_data["structure"] = content

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

    file_name = f"generate_story_structure-{retries}" if retries > 0 else f"generate_story_structure"
    utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
                   model=FIRST_PASS_GENERATION_MODEL,
                   settings={}, response_format=response_format, duration=elapsed)


def generate_characters(client: openai.Client, story_root: Path):
    # Load story-specific content.
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = yaml.safe_load(f)

    instructions = f"""
    Generate a list of the characters in this story. Define the protagonist, their allies, love interests, friends, 
    family, enemies, and people who pose as obstacles. 
    
    What are the ages of these characters. 
    Do they have any personality quirks that help define them? 
    What sort of physical features make them stand out to the reader?
    
    Define as many characters as possible.

    Story Details:
    Title: {story_data['general']['title']}
    Genres: {story_data['general']['genres']}
    Themes: {story_data['general']['themes']}
    Synopsis: {story_data['general']['synopsis']}
    
    Story Structure:
    """
    for key, value in story_data['structure'].items():
        if not key.startswith('_'):
            instructions += f" {key}: {value}"

    response_format: dict = {
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
                    "required": ["name", "age", "reason in story", "description", "personality"]
                }
            }
        }
    }

    messages = [
                {
                    "role": "system",
                    "content": GENERAL_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": instructions
                }
            ]

    content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
                                           response_format=response_format)
    story_data["characters"] = content

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

    file_name = f"generate_characters-{retries}" if retries > 0 else f"generate_characters"
    utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
                   model=FIRST_PASS_GENERATION_MODEL,
                   settings={}, response_format=response_format, duration=elapsed)


def generate_chapters(client: openai.Client, story_root: Path):
    # Load story-specific content.
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = yaml.safe_load(f)

    instructions = f"""
    Generate between 5 and 10 high-level chapters. Chapters will be broken up into scenes in the future, so these 
    chapters should be considered more higher level or more generic. Use the Title, Genres, Themes,
    general story synopsis, and story structure/outline to generate a number 
    of chapters. Chapters should span from the beginning to the end of the story. 
    
    Define the location the chapter takes place in.
    Define which characters feature in each chapter.
    Define which story structure point the chapter covers. 
    Multiple chapters can cover the same story structure parts.
    
    Story Details:
    Title: {story_data['general']['title']}
    Genres: {story_data['general']['genres']}
    Themes: {story_data['general']['themes']}
    Synopsis: {story_data['general']['synopsis']}
    
    Story Structure/Outline:
    Structure:
    """
    for key, value in story_data['structure'].items():
        instructions += f" {key}: {value}"

    response_format: dict = {
        "type": "json_schema",
        "json_schema": {
            "name": "output",
            "strict": "true",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "chapter number": {
                            "type": "integer"
                        },
                        "title": {
                            "type": "string"
                        },
                        "location": {
                            "type": "string"
                        },
                        "story structure point": {
                            "description": "The relevant story structure point for this chapter.",
                            "type": "string"
                        },
                        "characters": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "synopsis": {
                            "type": "string"
                        }
                    },
                    "required": ["chapter number", "title", "location",
                                 "story structure point", "characters", "synopsis"]
                }
            }
        }
    }

    messages = [
                {
                    "role": "system",
                    "content": GENERAL_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": instructions
                }
            ]

    content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
                                           response_format=response_format)
    story_data["chapters"] = content

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

    file_name = f"generate_chapters-{retries}" if retries > 0 else f"generate_chapters"
    utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
                   model=FIRST_PASS_GENERATION_MODEL,
                   settings={}, response_format=response_format, duration=elapsed)

# def expand_location(client: openai.Client, story_dir: Path):
#     start = time.time()
#
#     model = FIRST_PASS_GENERATION_MODEL
#
#     # Load story-specific content.
#     with open(story_dir / "overview.yaml", mode="r", encoding="utf-8") as f:
#         story_overview = yaml.safe_load(f)
#         if not story_overview:
#             raise Exception("Story Overview file does not exist, create a new story before generating the structure.")
#
#     with open(story_dir / "chapters.yaml", mode="r", encoding="utf-8") as f:
#         story_chapters = yaml.safe_load(f)
#         if not story_chapters:
#             raise Exception("Story Chapter file does not exist. Pending what to direct user to do.")
#     print(story_chapters)
#
#     with open(story_dir / "characters.yaml", mode="r", encoding="utf-8") as f:
#         story_characters = yaml.safe_load(f)
#         if not story_characters:
#             raise Exception("Story Characters file does not exist. Pending what to direct user to do.")
#     print(story_characters)
#
#     for chapter in story_chapters['chapters']:
#         detailed_chapter_characters = []
#
#         for character in chapter['characters']:
#             """
#             If a character is in the chapter, extract it's details from the characters.yaml object.
#             Combine the character object detail into a string for the LLM instructions.
#             """
#             char_data = [char for char in story_characters['characters'] if char['name'] in character]
#             char_str = ""
#             if len(char_data) == 1:
#                 for key, val in char_data[0].items():
#                     char_str += f"{key}: {val}\n"
#
#             char_str += "\n"
#
#             if char_str:
#                 detailed_chapter_characters.append(char_str)
#
#         instructions = f"""
#             Expand this chapter's location based on the chapter synopsis, theme, and characters.
#
#             Story Details:
#             Chapter Title: {chapter['title']}
#             Genres: {story_overview['genres']}
#             Themes: {story_overview['themes']}
#             Synopsis: {chapter['synopsis']}
#
#             Characters:
#
#
#             Locations:
#             {chapter['location']}
#         """
#
#     response_format: dict = {
#         "type": "json_schema",
#         "json_schema": {
#             "name": "locations",
#             "strict": "true",
#             "schema": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "location": {
#                                     "type": "integer"
#                                 },
#                                 "reason for location": {
#                                     "type": "array",
#                                     "items": {
#                                         "type": "string"
#                                     }
#                                 },
#                                 "events": {
#                                     "type": "array",
#                                     "items": {
#                                         "type": "string"
#                                     }
#                                 }
#                             },
#                             "required": ["location", "reason for location", "events"]
#                         }
#                     }
#                 }
#             }
#         }
#     }


#     response = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": GENERAL_SYSTEM_PROMPT
#             },
#             {
#                 "role": "user",
#                 "content": instructions
#             }
#         ],
#         model=model,
#         response_format=response_format
#     )
#     elapsed = time.time() - start
#
#     output = response.choices[0]
#     if output.message.role == "assistant":
#         content_str = output.message.content
#
#         from pprint import pprint
#         pprint(json.loads(content_str), sort_dicts=False)
#
#         if content_str:
#             content = json.loads(content_str)
#             
#
#             with open(story_dir / "locations.yaml", mode="w+", encoding="utf-8") as f:
#                 yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)
#
#             utils.log_step(
#                 story_root=story_dir, file_name="expand_locations", model=model,
#                 system_prompt=GENERAL_SYSTEM_PROMPT, instructions=instructions, settings={},
#                 response_format=response_format, duration=elapsed
#             )


def generate_scenes_for_chapter(client: openai.Client, story_root: Path):
    """
    For each chapter, generate a few scenes based on the chapter synopsis, location, and characters.
    """
    # Load story-specific content.
    with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
        story_data = yaml.safe_load(f)

    # Generate a non-json string block to seed the context before each scene.
    story_characters_str = ""
    for character in story_data['characters']:
        for key, val in character.items():
            story_characters_str += f"{key}: {val}\n"
        story_characters_str += "\n"

    story_structure_str = "\n".join(
        [f"{key}: {val}" for key, val in story_data['structure'].items() if not key == 'model'])

    pre_generation_seed_context = f"""
        Characters: {story_characters_str}
        Story Structure/Outline: {story_structure_str}
    """
    # End of context-seeding instructions

    for chapter in story_data['chapters']:
        instructions = f"""
        Generate at least 5 expanded scenes, in order, for this chapter. Go into more detail, describing
        the story in more detail, encapsulated within the scene. Output the location the scene takes
        place in, the characters in the scene, and the story beats detailing the events happening. 
        
        Story Themes: {story_data['general']['themes']}
        Story Genre: {" ,".join(story_data['general']['genres'])}
        Story Synopsis: {" ,".join(story_data['general']['synopsis'])}
                    
        Chapter Number: {chapter['chapter number']}
        Chapter Title: {chapter['title']}
        Chapter Story Structure reference: {chapter['story structure point']}
        Characters: {" ,".join(chapter['characters'])}
        Locations: {" ,".join(chapter['location'])}
        Synopsis: {chapter["synopsis"]}
        """

        response_format: dict = {
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
                }
            }
        }

        messages = [
                    {
                        "role": "system",
                        "content": GENERAL_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": pre_generation_seed_context
                    },
                    {
                        "role": "user",
                        "content": instructions
                    }
                ]

        while True:
            content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
                                                   response_format=response_format)

            if len(content) > 4:
                content["chapter number"] = chapter["chapter number"]
                break

        chapter["scenes"] = content

        with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
            yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

        file_name = f"generate_scenes_for_chapter_{chapter['chapter number']}-{retries}" if retries > 0 else f"generate_scenes_for_chapter_{chapter['chapter number']}"
        utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
                       model=FIRST_PASS_GENERATION_MODEL,
                       settings={}, response_format=response_format, duration=elapsed)


# response_format: dict = {
#     "type": "json_schema",
#     "json_schema": {
#         "name": "scenes",
#         "strict": "true",
#         "schema": {
#             "type": "object",
#             "properties": {
#                 "scenes": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "properties": {
#                             "chapter number": {
#                                 "type": "integer"
#                             },
#                             "scene number": {
#                                 "type": "integer"
#                             },
#                             "characters": {
#                                 "type": "array",
#                                 "items": {
#                                     "type": "string"
#                                 }
#                             },
#                             "location": {
#                                 "type": "string"
#                             },
#                             "story beats": {
#                                 "type": "string"
#                             }
#                         },
#                         "required": ["chapter number", "scene number", "characters", "location", "story beats"]
#                     }
#                 }
#             }
#         }
#     }
# }

if __name__ == '__main__':
    client = openai.Client(base_url="http://localhost:11434/v1", api_key="lm-studio")

    prompt = """
    Create a story about a cat with superpowers.
    """
    #
    # current_story = "Whisker's Awakening"
    # story_path = story_root = Path(f"{Path(__file__).parents[1]}/stories/{current_story}")

    story_path = expand_initial_prompt(client=client, user_prompt=prompt.strip())
    generate_story_structure(client=client, story_root=story_path, story_structure=StoryStructure.SEVEN_POINT)
    generate_characters(client=client, story_root=story_path)
    generate_chapters(client=client, story_root=story_path)
    generate_scenes_for_chapter(client=client, story_root=story_path)
