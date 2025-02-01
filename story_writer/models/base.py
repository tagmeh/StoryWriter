import json
import logging
from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel

from story_writer import settings

log = logging.getLogger(__name__)

CBM = TypeVar("CBM", bound="CustomBaseModel")


class CustomBaseModel(BaseModel):
    def list_key_values_str(self) -> str:
        """
        Used to dump a pydantic model into an LLM prompt as seed data.
        Use a `"".join([model.list_key_values_str for model in parent_model.child_model_array])`
          when converting an array of models into an array of formatted strings.

        Example output (of the 7 Pinch Point Structure Model):
         hook: In the sprawling metropolis of Purrth, <truncated> extraordinary superhero 'Feline Fury'.
         plot_turn_1: Kit gains her powers after <truncated> where felines hold power.
         pinch_point_1: As Kit continues to battle crime, <truncated> grapples with her own identity.
         mid_point: Kit uncovers the sinister source <truncated> truly making a difference in Purrth.
         pinch_point_2: With newfound clarity, <truncated> her powers to create a stronger force for good.
         plot_turn_2: Kit and her team face their <truncated> the victory comes at great personal cost for Kit.
         resolution: In the aftermath of the battle, <truncated> divided communities under one common cause.
        :return:
        """
        output = ""
        for key, value in self.model_dump(mode="python").items():
            if not key.startswith("_"):
                output += f" {key}: {value}\n"
        return output

    def save_to_file(self, output_dir: Path, filename: str = None):
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / (
            f"{filename}.{settings.SAVE_STORY_FILE_TYPE}"
            or f"{self.__class__.__name__}.{settings.SAVE_STORY_FILE_TYPE}"
        )
        log.debug(f"Saving/Updating outline data to {file_path}")
        try:
            if settings.SAVE_STORY_FILE_TYPE == "json":
                with open(file_path, mode="w+", encoding="utf-8") as f:
                    json.dump(self.model_dump(mode="json"), f, indent=4)

            elif settings.SAVE_STORY_FILE_TYPE == "yaml":
                with open(file_path, mode="w+", encoding="utf-8") as f:
                    yaml.dump(self.model_dump(mode="json"), f, default_flow_style=False, sort_keys=False)

        except Exception as err:
            log.error(f"Unable to save file '{file_path}' due to error: {err}")
            raise

    @classmethod
    def load_from_file(cls: type[CBM], story_dir: Path, filename: str) -> CBM:
        """
        Loads the data from a single file.
        :param story_dir: Path to story root directory
        :param filename: filename of the saved file.
        :return:
        """
        file_path = story_dir / f"{filename}.{settings.SAVE_STORY_FILE_TYPE}"
        log.debug(f"Loading outline data from '{file_path}'")

        try:
            if settings.SAVE_STORY_FILE_TYPE == "json":
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)

            elif settings.SAVE_STORY_FILE_TYPE == "yaml":
                with open(file_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)

        except Exception as err:
            log.error(f"Failed to load story data due to error: {err}")
            raise

        return cls(**data)


class StoryStructure(CustomBaseModel):
    style: str  # Name of the story structure style/format
