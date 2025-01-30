import logging

from story_writer.config import models
from story_writer.config import story_settings as ss
from story_writer.story_config import StoryConfig

console_handler = logging.StreamHandler()
# TODO: Add color to formatting? Tried "colorlog", doesn't seem to work for Windows. /shrug
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

settings_config = {
    "STORY_STRUCTURE_STYLE": ss.STORY_STRUCTURE_STYLE,
    "CHAPTER_MINIMUM_COUNT": ss.CHAPTER_MINIMUM_COUNT,
    "SCENES_PER_CHAPTER_MINIMUM_COUNT": ss.SCENES_PER_CHAPTER_MINIMUM_COUNT,
    "STAGE": ss.OUTLINE_STAGE_CONFIGS,
    "SAVE_STORY_FILE_TYPE": ss.SAVE_STORY_FILE_TYPE,
    "CONSOLIDATE_SAVED_OUTPUT": ss.CONSOLIDATE_SAVED_OUTPUT,
    "SCENES_PER_CHAPTER_RETRY_COUNT": ss.SCENES_PER_CHAPTER_RETRY_COUNT,
    "LLM_INVALID_OUTPUT_RETRY_COUNT": ss.LLM_INVALID_OUTPUT_RETRY_COUNT,
    "LLM_EMPTY_OUTPUT_RETRY_COUNT": ss.LLM_INVALID_OUTPUT_RETRY_COUNT,
    "MAX_TOKENS": ss.MAX_TOKENS,
    "MODEL": models.FIRST_PASS_GENERATION_MODEL,
}

settings = StoryConfig(**settings_config)
