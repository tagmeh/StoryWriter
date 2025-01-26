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

    content, elapsed, retries = stream_llm(client=client, messages=messages, model=FIRST_PASS_GENERATION_MODEL,
                                           response_format=response_format)
    story_data["chapters"] = content

    with open(story_root / "story_data.yaml", mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

    file_name = f"generate_chapters-{retries}" if retries > 0 else f"generate_chapters"
    utils.log_step(story_root=story_root, messages=messages, file_name=file_name,
                   model=FIRST_PASS_GENERATION_MODEL,
                   settings={}, response_format=response_format, duration=elapsed)