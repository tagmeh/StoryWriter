import json
import logging
from pathlib import Path

import yaml

from story_writer.story_data_model import StoryData

log = logging.getLogger(__name__)


# TODO: Update settings such that it's passed into the llm call and logged.
#  Settings might be anything beyond the absolute required inputs, like "stream" and "stream_options".
def log_step(
    story_root: Path,
    file_name: str,
    model: str,
    messages: list,
    settings: dict,
    response_format: dict,
    duration: float,
):
    """
    Generates logs per-story in order to inspect the inputs and outputs of the LLM calls, per function.

    :param messages:
    :param story_root:
    :param file_name:
    :param model:
    :param settings:
    :param response_format:
    :param duration:

    :return:
    """
    story_log_dir = story_root / "logs"
    story_log_dir.mkdir(parents=True, exist_ok=True)

    obj = {
        "messages": messages,
        "model": model,
        "settings": settings,
        "response_format": response_format,
        "response_time": duration,
    }

    with open(story_log_dir / f"{file_name}.json", mode="w+", encoding="utf-8") as f:
        json.dump(obj, f, indent=4)


def load_story_data(story_path: Path):
    story_data_path = story_path / "story_data.yaml"
    log.debug(f"Loading story data from '{story_data_path}'")
    with open(story_data_path, encoding="utf-8") as f:
        return StoryData(**yaml.safe_load(f))


def save_story_data(story_path: Path, story_data: StoryData) -> None:
    """
    Saves the current state of the StoryData instance. This is used as a cache/save point while gathering data.

    :param story_path: Path - Path to the root /stories/ directory where the story output is stored.
    :param story_data: StoryData - Pydantic model representation of the cached/saved story data.
    :return: None
    """
    story_data_path = story_path / "story_data.yaml"
    log.debug(f'Saving/Updating story data to {story_path / "story_data.yaml"}')

    # TODO: May update this section to allow for json or yaml outputs dictated by user setting.
    with open(story_data_path, mode="w+", encoding="utf-8") as f:
        yaml.dump(story_data.model_dump(mode="json"), f, default_flow_style=False, sort_keys=False)

    log.debug(f"Saved/Updated story data for story: '{story_data.general.title}'")
