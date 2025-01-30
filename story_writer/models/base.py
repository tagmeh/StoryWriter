import json
import logging
from pathlib import Path
from typing import Literal, TypeVar

import yaml
from pydantic import BaseModel

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

    def save_to_file(self, output_dir: Path, file_type: str, filename: str = None):
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / (f"{filename}.{file_type}" or f"{self.__class__.__name__}.{file_type}")

        try:
            if file_type == "json":
                with open(file_path, mode="w+", encoding="utf-8") as f:
                    json.dump(self.model_dump(mode="json"), f, indent=4)
            elif file_type == "yaml":
                with open(file_path, mode="w+", encoding="utf-8") as f:
                    yaml.dump(self.model_dump(mode="json"), f, default_flow_style=False, sort_keys=False)
        except Exception as err:
            log.error(f"Unable to save file '{file_path}' due to error: {err}")
            raise

    @classmethod
    def load_from_file(cls: type[CBM], file_type: Literal["json", "yaml"], file_path: Path) -> CBM:
        if file_type == "json":
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
        elif file_type == "yaml":
            with open(file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        else:
            raise Exception(f"File type: '{file_type}' not supported.")

        return cls(**data)


class StoryStructure(CustomBaseModel):
    style: str  # Name of the story structure style/format
