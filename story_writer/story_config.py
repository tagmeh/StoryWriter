from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from story_writer.config import models
from story_writer.constants import StorySaveFormatEnum, StoryStructureEnum


class OutlineStageConfig(BaseModel):
    """
    Settings for chat completion. This setting is applied to each stage in the outline creation process.

    https://github.com/openai/openai-python/blob/main/src/openai/types/completion_create_params.py
    """

    MODEL: str | None = None
    TEMPERATURE: float = Field(default=0.95, gt=0, le=1.0)
    MAX_TOKENS: int = Field(default=1024, gt=0)
    STREAM: bool = Field(default=False)
    FREQUENCY_PENALTY: float = Field(default=1.3, ge=-2.0, le=2.0)


class OutlineConfig(BaseModel):
    GENERAL: OutlineStageConfig
    STRUCTURE: OutlineStageConfig
    CHARACTERS: OutlineStageConfig
    WORLDBUILDING: OutlineStageConfig
    CHAPTERS: OutlineStageConfig
    SCENES: OutlineStageConfig


class StoryConfig(BaseSettings):
    STORY_STRUCTURE_STYLE: StoryStructureEnum = Field(default=StoryStructureEnum.SEVEN_POINT)
    CHAPTER_MINIMUM_COUNT: int = Field(default=5, gt=-1)
    SCENES_PER_CHAPTER_MINIMUM_COUNT: int = Field(default=3)
    STAGE: OutlineConfig
    SAVE_STORY_FILE_TYPE: StorySaveFormatEnum = Field(default=StorySaveFormatEnum.JSON)
    CONSOLIDATE_SAVED_OUTPUT: bool = Field(default=True)
    SCENES_PER_CHAPTER_RETRY_COUNT: int = Field(default=30, gt=0)
    LLM_INVALID_OUTPUT_RETRY_COUNT: int = Field(default=10, gt=0)
    LLM_EMPTY_OUTPUT_RETRY_COUNT: int = Field(default=10, gt=0)
    TEMPERATURE: float = Field(default=0.95, gt=0, le=1.0)
    MODEL: str = Field(default=models.FIRST_PASS_GENERATION_MODEL)
    MAX_TOKENS: int = Field(default=2048)
    STREAM: bool = Field(default=True)
