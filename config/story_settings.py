from story_writer.story_structures import StoryStructure

# STORY SETTINGS ======================================================================
# The type of outline/structure generated to help keep the outline on track.
STORY_STRUCTURE_STYLE: StoryStructure = StoryStructure.SEVEN_POINT

# Minimum required chapters for the outline.
CHAPTER_MINIMUM_COUNT = 5

# Minimum number of scenes required for each chapter.
SCENES_PER_CHAPTER_MINIMUM_COUNT = 3


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
