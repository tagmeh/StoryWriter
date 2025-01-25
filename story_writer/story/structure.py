# def generate_story_structure(client: openai.Client, story_root: Path, story_structure: Optional[StoryStructure] = None):
#     start = time.time()
#
#     story_structure = story_structure or StoryStructure.CLASSIC
#
#     # Load story-specific content.
#     with open(story_root / "story_data.yaml", mode="r", encoding="utf-8") as f:
#         story_data = yaml.safe_load(f)
#
#     if not story_data["general"]:
#         raise Exception("General story details do not exist, create a new story before generating the story structure.")
#
#     instructions = f"""
#     Generate a story structure/outline using the following story structure style: {story_structure.value}.
#     Expand on each point in the story, adding details where appropriate. Avoid dialogue at this stage.
#
#     Consider the protagonist's motivations and desires.
#     What issues does the protagonist run into, how do they overcome them?
#     Does anyone help or hinder the protagonist?
#
#     User Input:
#     Title: {story_data["general"]['title']}
#     Genres: {story_data["general"]['genres']}
#     Themes: {story_data["general"]['themes']}
#     Synopsis: {story_data["general"]['synopsis']}
#     """
#
#     response_format: dict = story_structure_schema
#     response_format["json_schema"]["schema"] = get_story_structure_schema(story_structure)
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
#     story_data["structure"] = content
#
#     with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
#         yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)
#
#     file_name = f"generate_story_structure-{retries}" if retries > 0 else f"generate_story_structure"
#     utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
#                    model=FIRST_PASS_GENERATION_MODEL,
#                    settings={}, response_format=response_format, duration=elapsed)
