from story_writer.constants import StorySaveFormatEnum, StoryStructureEnum

# STORY SETTINGS ======================================================================
# The type of outline/structure generated to help keep the outline on track.
STORY_STRUCTURE_STYLE: StoryStructureEnum = StoryStructureEnum.SEVEN_POINT

# Minimum required chapters for the outline.
CHAPTER_MINIMUM_COUNT = 5

# Minimum number of scenes required for each chapter.
SCENES_PER_CHAPTER_MINIMUM_COUNT = 3

# Some models can get stuck generating infinite output if not limited in some way.
OUTLINE_STAGE_CONFIGS = {
    "GENERAL": {"model": None, "temperature": 0.95, "stream": True, "max_tokens": 1024},
    "STRUCTURE": {"max_tokens": 1024},
    "CHARACTERS": {"max_tokens": 2048},
    "WORLDBUILDING": {"max_tokens": 2048},
    "CHAPTERS": {"max_tokens": 2048},
    "SCENES": {"max_tokens": 2048},
}

# SYSTEM SETTINGS =====================================================================
# File format that the story_data (or the separate files) are saved as.
SAVE_STORY_FILE_TYPE = StorySaveFormatEnum.JSON  # JSON or YAML

# If False, will save each of the different sections of the story_data as their own files general, structure, etc
# Saving as multiple files may make it easier to edit sections.
CONSOLIDATE_SAVED_OUTPUT = True

# TODO: Add -1 option to try forever.
#  Add warning that this will create an infinite loop, until such a time that the data is collected.
# LLM VALIDATION SETTINGS =============================================================
# How many times will it try to generate the scenes.
#  Will retry if the generated scenes are fewer than SCENES_PER_CHAPTER_MINIMUM_COUNT.
SCENES_PER_CHAPTER_RETRY_COUNT = 30

# Num of retries if the generated output fails the pydantic model validation.
LLM_INVALID_OUTPUT_RETRY_COUNT = 10

# Num of retries if the LLM returns empty data or fails the json.loads().
LLM_EMPTY_OUTPUT_RETRY_COUNT = 10

# Token Limit to apply to every LLM call. Overwritten by the OUTLINE_STAGE_CONFIGS stage "token_limit" setting.
LLM_TOKEN_LIMIT = 2048

TEMPERATURE = 0.95
