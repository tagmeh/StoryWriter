import logging
import re
from typing import Annotated

from pydantic import AfterValidator, Field, field_validator

from story_writer.models.base import CustomBaseModel
from story_writer.models.validations import str_not_empty

log = logging.getLogger(__name__)


class GeneralData(CustomBaseModel):
    """
    A model to represent the general details of a outline as defined by the structured output of an LLM.
    This model must match the json schema of the LLM's response_format input.
    """

    title: Annotated[str, AfterValidator(str_not_empty), Field(description="The title of the story.")]
    themes: list[Annotated[str, AfterValidator(str_not_empty)]]
    genres: list[Annotated[str, AfterValidator(str_not_empty)]]
    synopsis: Annotated[str, AfterValidator(str_not_empty)]

    @field_validator("title")
    @classmethod
    def clean_title(cls, value):
        value.strip()
        if ":" in value:
            """Windows directories cannot contain colons (:)."""
            value = re.sub(":", " -", value)
        return value

    @field_validator("themes", "genres")
    @classmethod
    def clean_array(cls, value):
        """
        Account for some of the weird ways the LLM outputs sometimes.

        Examples: ["Self-discovery | Friendship | Redemption"]
        """
        for item in value:
            if "|" in item:  # Sometimes the LLM separates strings with a pipe. /shrug
                sub_values = item.split("|")
                value.remove(item)
                value.extend(sub_values)

        # Clean up any whitespace.
        for item in value:
            item.strip()

        return value
