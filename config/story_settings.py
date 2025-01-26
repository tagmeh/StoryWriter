from story_writer.story_structures import StoryStructure

# STORY SETTINGS ======================================================================
# The type of outline/structure generated to help keep the story on track.
STORY_STRUCTURE_STYLE: StoryStructure = StoryStructure.CLASSIC

# Minimum required chapters for the story.
CHAPTER_MINIMUM_COUNT = 5

# Minimum number of scenes required for each chapter.
SCENES_PER_CHAPTER_MINIMUM_COUNT = 4


# LLM VALIDATION SETTINGS =============================================================
# How many times will it try to generate the scenes.
#  Will retry if the generated scenes are fewer than SCENES_PER_CHAPTER_MINIMUM_COUNT.
SCENES_PER_CHAPTER_RETRY_COUNT = 10

# Num of retries if the generated output fails the pydantic model validation.
LLM_INVALID_OUTPUT_RETRY_COUNT = 10

# Num of retries if the LLM returns empty data or fails the json.loads().
LLM_EMPTY_OUTPUT_RETRY_COUNT = 10
