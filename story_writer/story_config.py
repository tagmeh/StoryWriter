import logging
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from story_writer.constants import StorySaveFormatEnum, StoryStructureEnum

log = logging.getLogger(__name__)


class OverrideSettingsBase(BaseModel):
    """Holds validations for the two similar settings classes."""

    class Config:
        extra = "allow"


class StageOverrideSettings(OverrideSettingsBase):
    """
    Override settings for each stage in the outline process.
    Update the config.yaml for each stage to override.
        ex:
        STAGE:
          GENERAL:
            temperature: 1.0
            max_tokens: 100
    Supported settings can be found here:
    https://platform.openai.com/docs/api-reference/chat
    """

    stream: bool | None = None
    max_tokens: int | None = None
    model: str | None = None
    temperature: float | None = None
    frequency_penalty: float | None = None


class OpenAiChatCompletionSettings(OverrideSettingsBase):
    """
    Default OpenAI Completions.create() parameters. Passed into the function as kwargs directly.
    Allows extra params for edge case support. Update the config.yaml under
    "LLM" to add additional supported properties.
    Supported settings can be found here:
    https://platform.openai.com/docs/api-reference/chat
    """

    model: str
    reasoning_effort: Literal["low", "medium", "high"] = Field(
        default="medium", description="Lower reasoning means faster results."
    )
    modalities: list[str] = ["text"]  # This project does not support audio yet.
    stream: bool = Field(default=False)
    max_tokens: int = Field(default=2048)
    temperature: float = Field(default=0.95, gt=0, le=2.0)
    top_p: float = Field(default=1.0)
    presence_penalty: float = Field(default=1.0, ge=-2.0, le=2.0)
    n: int | None = Field(default=1, ge=1, description="Number of chat completions to create per call.")


class OutlineConfig(BaseModel):
    GENERAL: StageOverrideSettings = StageOverrideSettings()
    STRUCTURE: StageOverrideSettings = StageOverrideSettings()
    CHARACTERS: StageOverrideSettings = StageOverrideSettings()
    WORLDBUILDING: StageOverrideSettings = StageOverrideSettings()
    CHAPTERS: StageOverrideSettings = StageOverrideSettings()
    SCENES: StageOverrideSettings = StageOverrideSettings()


class Settings(BaseSettings):
    BASIC_SYSTEM_PROMPT: str = Field(
        default="You are an experienced story author. You fill your story "
        "with worldbuilding and character defining details to fill out the story."
    )
    # URL to the LLM instance, local or remote.
    LLM_URL: str = Field(default="http://localhost:1234/v1")
    # API Key for LLM platform. Can also use a .env file with API_KEY
    API_KEY: str = Field(default="LM Studio")
    # The type of outline/structure generated to help keep the outline on track.
    STORY_STRUCTURE_STYLE: StoryStructureEnum = Field(default=StoryStructureEnum.SEVEN_POINT_STORY_STRUCTURE)
    # Minimum required chapters for the outline.
    CHAPTER_MINIMUM_COUNT: int = Field(default=5, ge=1)
    # Minimum number of scenes required for each chapter.
    SCENES_PER_CHAPTER_MINIMUM_COUNT: int = Field(default=3, ge=1)
    # File format that the story_data (or the separate files) are saved as.
    SAVE_STORY_FILE_TYPE: StorySaveFormatEnum = Field(default=StorySaveFormatEnum.JSON)
    # True: Saves all outline data into one story_data.json|yaml file.
    # False: Saves each outline component in separate files. Chapters/Scenes are saved in directories.
    CONSOLIDATE_SAVED_OUTPUT: bool = Field(default=True)
    # Number of retries to generate the scenes data. This section has proven to be particularly finicky.
    #  Will retry if the generated scenes are fewer than SCENES_PER_CHAPTER_MINIMUM_COUNT.
    SCENES_PER_CHAPTER_RETRY_COUNT: int = Field(default=30, gt=0)
    # Number of times to retry the chat completion upon pydantic model validation failure.
    LLM_INVALID_OUTPUT_RETRY_COUNT: int = Field(default=10, gt=0)
    # Number of times to retry the chat completion upon receiving an empty output or bad json data (
    #   if validating a structured output against a pydantic model.).
    LLM_EMPTY_OUTPUT_RETRY_COUNT: int = Field(default=10, gt=0)
    # Per-outline-stage settings.
    STAGE: OutlineConfig = OutlineConfig()
    # Default LLM Settings if not provided a per-STAGE setting to override it.
    LLM: OpenAiChatCompletionSettings

    class Config:
        extra = "ignore"
