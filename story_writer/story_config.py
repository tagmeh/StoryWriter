import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from story_writer.constants import StoryStructureEnum

log = logging.getLogger(__name__)


class OverrideSettingsBase(BaseModel):
    """Holds validations for the two similar settings classes."""

    class Config:
        extra = "allow"  # Required to allow users to use undefined settings that are supported by the OpenAI package.


class StageOverrideSettings(OverrideSettingsBase):
    """
    Override settings for each stage in the outline process.
    Update the config.yaml for each stage to override.
        ex:
        stage:
          general:
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
    # User Defined Settings that I didn't explicitly set
    # OpenAI supports more settings than I have set, and
    # I don't need to recreate their stuff.


class OpenAiChatDefaultSettings(OverrideSettingsBase):
    """
    Default OpenAI Completions.create() parameters. Passed into the function as kwargs directly.
    Allows extra params for edge case support. Update the config.yaml under
    "llm" to add additional supported properties.
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
    general: StageOverrideSettings = StageOverrideSettings()
    structure: StageOverrideSettings = StageOverrideSettings()
    characters: StageOverrideSettings = StageOverrideSettings()
    worldbuilding: StageOverrideSettings = StageOverrideSettings()
    chapters: StageOverrideSettings = StageOverrideSettings()
    scenes: StageOverrideSettings = StageOverrideSettings()


class StoryStats(BaseModel):
    scene_count: int
    character_count: int
    chapter_count: int
    word_count: int


class Settings(BaseSettings):
    story_dir: Path | None = None
    basic_system_prompt: str = Field(
        default="You are an experienced story author. You fill your story "
        "with worldbuilding and character defining details to fill out the story."
    )
    # URL to the LLM instance, local or remote.
    llm_url: str = Field(default="http://localhost:1234/v1")
    # API Key for LLM platform. Can also use a .env file with API_KEY
    api_key: str = Field(default="LM Studio")
    # The type of outline/structure generated to help keep the outline on track.
    story_structure_style: StoryStructureEnum = Field(default=StoryStructureEnum.SEVEN_POINT_STORY_STRUCTURE)
    # Minimum required chapters for the outline.
    chapter_minimum_count: int = Field(default=5, ge=1)
    # Minimum number of scenes required for each chapter.
    scenes_per_chapter_minimum_count: int = Field(default=3, ge=1)
    # File format that the story_data (or the separate files) are saved as.
    save_story_file_type: Literal["json", "yaml"] = "yaml"
    # True: Saves all outline data into one story_data.json|yaml file.
    # False: Saves each outline component in separate files. Chapters/Scenes are saved in directories.
    consolidate_saved_output: bool = Field(default=True)
    # Number of retries to generate the scenes data. This section has proven to be particularly finicky.
    #  Will retry if the generated scenes are fewer than SCENES_PER_CHAPTER_MINIMUM_COUNT.
    scenes_per_chapter_retry_count: int = Field(default=30, gt=0)
    # Number of times to retry the chat completion upon pydantic model validation failure.
    llm_invalid_output_retry_count: int = Field(default=10, gt=0)
    # Number of times to retry the chat completion upon receiving an empty output or bad json data (
    #   if validating a structured output against a pydantic model.).
    llm_empty_output_retry_count: int = Field(default=10, gt=0)
    # Per-outline-stage settings.
    stage: OutlineConfig = OutlineConfig()
    # Default LLM Settings if not provided a per-STAGE setting to override it.
    llm: OpenAiChatDefaultSettings
    draft: StageOverrideSettings = StageOverrideSettings()

    class Config:
        extra = "ignore"
