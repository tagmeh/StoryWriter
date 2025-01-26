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