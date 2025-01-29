import json
import logging
from pathlib import Path
from typing import Type, TYPE_CHECKING

from pydantic import BaseModel

from story_writer.constants import StoryStructureEnum
from story_writer.story_data_model import create_json_schema, STORY_STYLE_MODEL_MAPPING

if TYPE_CHECKING:
    from story_writer.story_data_model import StoryStructure

log = logging.getLogger(__name__)


# TODO: Update settings such that it's passed into the llm call and logged.
#  Settings might be anything beyond the absolute required inputs, like "stream" and "stream_options".
def log_step(
        story_root: Path,
        file_name: str,
        model: str,
        messages: list,
        settings: dict,
        duration: float,
        response_model: Type[BaseModel] | None = None,
):
    """
    Generates logs per-outline in order to inspect the inputs and outputs of the LLM calls, per function.

    :param messages:
    :param story_root:
    :param file_name:
    :param model:
    :param settings:
    :param response_model:
    :param duration:

    :return:
    """
    story_log_dir = story_root / "logs"
    story_log_dir.mkdir(parents=True, exist_ok=True)

    obj = {
        "messages": messages,
        "model": model,
        "settings": settings,
        "response_format": create_json_schema(response_model),
        "response_time": duration,
    }

    with open(story_log_dir / f"{file_name}.json", mode="w+", encoding="utf-8") as f:
        json.dump(obj, f, indent=4)


# def load_story_data(story_path: Path):
#     return StoryData.load_from_file(
#         saved_dir=story_path, file_type=SAVE_STORY_FILE_TYPE.value, one_file=CONSOLIDATE_SAVED_OUTPUT
#     )


# def save_story_data(story_path: Path, story_data: "StoryData") -> None:
#     """
#     Saves the current state of the StoryData instance. This is used as a cache/save point while gathering data.
#
#     :param story_path: Path - Path to the root /stories/ directory where the outline output is stored.
#     :param story_data: StoryData - Pydantic model representation of the cached/saved outline data.
#     :return: None
#     """
#     story_data.save_to_file(
#         output_dir=story_path, file_type=SAVE_STORY_FILE_TYPE.value, one_file=CONSOLIDATE_SAVED_OUTPUT
#     )
#     log.debug(f"Saved/Updated outline data for story: '{story_data.general.title}'")


def get_story_structure_model(story_structure_enum: StoryStructureEnum) -> Type["StoryStructure"]:
    if story_structure_enum not in STORY_STYLE_MODEL_MAPPING:
        raise ValueError(f"Invalid story structure provided: {story_structure_enum}")

    return STORY_STYLE_MODEL_MAPPING[story_structure_enum]
