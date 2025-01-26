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

        response_format: dict = story_chapter_scene_schema

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
