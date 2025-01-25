import json
from pathlib import Path
from typing import Optional


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
