"""
In the process of moving these functions into the story_writer/ directory
and hopefully organizing them better per the process to write a story.
"""


#
#
# def generate_characters(client: openai.Client, story_root: Path):
#     # Load story-specific content.
#     with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
#         story_data = yaml.safe_load(f)
#
#     instructions = f"""
#     Generate a list of the characters in this story. Define the protagonist, their allies, love interests, friends,
#     family, enemies, and people who pose as obstacles.
#
#     What are the ages of these characters.
#     Do they have any personality quirks that help define them?
#     What sort of physical features make them stand out to the reader?
#
#     Define as many characters as possible.
#
#     Story Details:
#     Title: {story_data['general']['title']}
#     Genres: {story_data['general']['genres']}
#     Themes: {story_data['general']['themes']}
#     Synopsis: {story_data['general']['synopsis']}
#
#     Story Structure:
#     """
#     for key, value in story_data['structure'].items():
#         if not key.startswith('_'):
#             instructions += f" {key}: {value}"
#
#     response_format: dict = story_characters_schema
#
#     messages = [
#         {
#             "role": "system",
#             "content": GENERAL_SYSTEM_PROMPT
#         },
#         {
#             "role": "user",
#             "content": instructions
#         }
#     ]
#
#     content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
#                                          response_format=response_format)
#     story_data["characters"] = content
#
#     with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
#         yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)
#
#     file_name = f"generate_characters-{retries}" if retries > 0 else f"generate_characters"
#     utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
#                    model=FIRST_PASS_GENERATION_MODEL,
#                    settings={}, response_format=response_format, duration=elapsed)
#
#
# def generate_chapters(client: openai.Client, story_root: Path):
#     # Load story-specific content.
#     with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
#         story_data = yaml.safe_load(f)
#
#     instructions = f"""
#     Generate between 5 and 10 high-level chapters. Chapters will be broken up into scenes in the future, so these
#     chapters should be considered more higher level or more generic. Use the Title, Genres, Themes,
#     general story synopsis, and story structure/outline to generate a number
#     of chapters. Chapters should span from the beginning to the end of the story.
#
#     Define the location the chapter takes place in.
#     Define which characters feature in each chapter.
#     Define which story structure point the chapter covers.
#     Multiple chapters can cover the same story structure parts.
#
#     Story Details:
#     Title: {story_data['general']['title']}
#     Genres: {story_data['general']['genres']}
#     Themes: {story_data['general']['themes']}
#     Synopsis: {story_data['general']['synopsis']}
#
#     Story Structure/Outline:
#     Structure:
#     """
#     for key, value in story_data['structure'].items():
#         instructions += f" {key}: {value}"
#
#     response_format: dict = story_chapters_schema
#
#     messages = [
#         {
#             "role": "system",
#             "content": GENERAL_SYSTEM_PROMPT
#         },
#         {
#             "role": "user",
#             "content": instructions
#         }
#     ]
#
#     content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
#                                          response_format=response_format)
#     story_data["chapters"] = content
#
#     with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
#         yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)
#
#     file_name = f"generate_chapters-{retries}" if retries > 0 else f"generate_chapters"
#     utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
#                    model=FIRST_PASS_GENERATION_MODEL,
#                    settings={}, response_format=response_format, duration=elapsed)

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
    # response_format: dict = {
    #     "type": "json_schema",
    #     "json_schema": {
    #         "name": "locations",
    #         "strict": "true",
    #         "schema": {
    #             "type": "array",
    #             "items": {
    #                 "type": "object",
    #                 "properties": {
    #                     "name": {
    #                         "type": "string"
    #                     },
    #                     "events": {
    #                         "type": "array",
    #                         "description": "Events that happen in this location",
    #                         "items": {
    #                             "type": "string"
    #                         }
    #                     }
    #                 },
    #                 "required": ["name", "events"]
    #             }
    #         }
    #     }
    # }


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


# def generate_scenes_for_chapter(client: openai.Client, story_root: Path):
#     """
#     For each chapter, generate a few scenes based on the chapter synopsis, location, and characters.
#     """
#     # Load story-specific content.
#     with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
#         story_data = yaml.safe_load(f)
#
#     # Generate a non-json string block to seed the context before each scene.
#     story_characters_str = ""
#     for character in story_data['characters']:
#         for key, val in character.items():
#             story_characters_str += f"{key}: {val}\n"
#         story_characters_str += "\n"
#
#     story_structure_str = "\n".join(
#         [f"{key}: {val}" for key, val in story_data['structure'].items() if not key == 'model'])
#
#     pre_generation_seed_context = f"""
#         Characters: {story_characters_str}
#         Story Structure/Outline: {story_structure_str}
#     """
#     # End of context-seeding instructions
#
#     for chapter in story_data['chapters']:
#         instructions = f"""
#         Generate at least 5 expanded scenes, in order, for this chapter. Go into more detail, describing
#         the story in more detail, encapsulated within the scene. Output the location the scene takes
#         place in, the characters in the scene, and the story beats detailing the events happening.
#
#         Story Themes: {story_data['general']['themes']}
#         Story Genre: {" ,".join(story_data['general']['genres'])}
#         Story Synopsis: {" ,".join(story_data['general']['synopsis'])}
#
#         Chapter Number: {chapter['chapter number']}
#         Chapter Title: {chapter['title']}
#         Chapter Story Structure reference: {chapter['story structure point']}
#         Characters: {" ,".join(chapter['characters'])}
#         Locations: {" ,".join(chapter['location'])}
#         Synopsis: {chapter["synopsis"]}
#         """
#
#         response_format: dict = story_chapter_scene_schema
#
#         messages = [
#             {
#                 "role": "system",
#                 "content": GENERAL_SYSTEM_PROMPT
#             },
#             {
#                 "role": "user",
#                 "content": pre_generation_seed_context
#             },
#             {
#                 "role": "user",
#                 "content": instructions
#             }
#         ]
#
#         while True:
#             content, elapsed, retries = call_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
#                                                  response_format=response_format)
#
#             if len(content) > 4:
#                 content["chapter number"] = chapter["chapter number"]
#                 break
#
#         chapter["scenes"] = content
#
#         with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
#             yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)
#
#         file_name = f"generate_scenes_for_chapter_{chapter['chapter number']}-{retries}" if retries > 0 else f"generate_scenes_for_chapter_{chapter['chapter number']}"
#         utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
#                        model=FIRST_PASS_GENERATION_MODEL,
#                        settings={}, response_format=response_format, duration=elapsed)


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

# if __name__ == '__main__':
    # client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    #
    # prompt = """
    # Create a story about a cat with superpowers.
    # """
    #
    # current_story = "Whisker's Awakening"
    # story_path = story_root = Path(f"{Path(__file__).parents[1]}/stories/{current_story}")

    # story_path = expand_initial_prompt(client=client, user_prompt=prompt.strip())
    # generate_story_structure(client=client, story_root=story_path, story_structure=StoryStructure.SEVEN_POINT)
    # generate_characters(client=client, story_root=story_path)
    # generate_chapters(client=client, story_root=story_path)
    # generate_scenes_for_chapter(client=client, story_root=story_path)
