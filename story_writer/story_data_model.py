import json
import logging
import re
from pathlib import Path
from typing import Annotated, Any, Generic, Literal, TypeVar

from pydantic import AfterValidator, BaseModel, field_validator

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
CBM = TypeVar("CBM", bound="CustomBaseModel")


# Todo: Determine if using this neat DeferredModel is needed for the StoryData model.
#  Problem: We wanted to validate the StoryData object, but for most of it's outline-generating
#  life, it was missing information. So it could only be validated once the outline is complete.
#  The DeferredModel object is a "DeferredModel" type until validated, in which case it becomes
#  a StoryData (or w/e normal type).
#  If we can wait until the outline is done to validate the StoryData, then why do we need this DeferredModel model?
class DeferredModel(Generic[T]):
    """https://github.com/pydantic/pydantic/issues/559#issuecomment-519686409"""

    def __init__(self, type_: type[T], kwargs: dict[str, Any]):
        self.type_ = type_
        self.kwargs = kwargs

    def validate(self) -> T:
        return self.type_(**self.kwargs)

    def __repr__(self):
        return f"{type(self).__name__}(type_={self.type_.__name__}, kwargs={self.kwargs})"


class DeferrableModel(BaseModel):
    @classmethod
    def defer(cls: type[T], **kwargs: Any) -> DeferredModel[T]:
        return DeferredModel(cls, kwargs)


def str_not_empty(value: str) -> str:
    """Prevents empty strings from being a valid input when requiring a string input."""
    if value == "":
        raise ValueError(f"'{value}' must not be empty.")
    return value


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
                    yaml.dump(story_data.model_dump(mode="json"), f, default_flow_style=False, sort_keys=False)
        except Exception:
            log.error(f"Unable to save file '{file_path}'")
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
    """
    Parent to all the outline structure types.
    """

    # Todo: Identify a way to generate a list of types of the classes that subclass StoryStructure to
    #  dynamically update the StoryStructureData.structure property. If possible.++
    ...


class ClassicStoryStructure(StoryStructure):
    exposition: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class ThreeActStructure(StoryStructure):
    act_1_exposition: str
    act_1_inciting_incident: str
    act_1_plot_point_1: str
    act_2_rising_action: str
    act_2_midpoint: str
    act_2_plot_point_2: str
    act_3_pre_climax: str
    act_3_climax: str
    act_3_denouement: str


class FiveActStructure(StoryStructure):
    exposition: str
    rising_action: str
    climax: str
    falling_action: str
    resolution: str


class SevenPointStoryStructure(StoryStructure):
    hook: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_1: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_1: Annotated[str, AfterValidator(str_not_empty)]
    mid_point: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_2: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_2: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class FreytagsPyramidStoryStructure(StoryStructure):
    exposition: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    denouement: Annotated[str, AfterValidator(str_not_empty)]


class TheHerosJourneyStoryStructure(StoryStructure):
    the_ordinary_world: Annotated[str, AfterValidator(str_not_empty)]
    the_call_to_adventure: Annotated[str, AfterValidator(str_not_empty)]
    the_refusal_of_the_call: Annotated[str, AfterValidator(str_not_empty)]
    meeting_the_mentor: Annotated[str, AfterValidator(str_not_empty)]
    crossing_the_threshold: Annotated[str, AfterValidator(str_not_empty)]
    tests_allies_enemies: Annotated[str, AfterValidator(str_not_empty)]
    approach_to_the_inmost_cave: Annotated[str, AfterValidator(str_not_empty)]
    the_ordeal: Annotated[str, AfterValidator(str_not_empty)]
    seizing_the_sword: Annotated[str, AfterValidator(str_not_empty)]
    the_road_back: Annotated[str, AfterValidator(str_not_empty)]
    resurrection: Annotated[str, AfterValidator(str_not_empty)]
    return_with_the_elixir: Annotated[str, AfterValidator(str_not_empty)]


class DanHarmonsStoryCircleStructure(StoryStructure):
    you: Annotated[str, AfterValidator(str_not_empty)]
    need: Annotated[str, AfterValidator(str_not_empty)]
    go: Annotated[str, AfterValidator(str_not_empty)]
    search: Annotated[str, AfterValidator(str_not_empty)]
    find: Annotated[str, AfterValidator(str_not_empty)]
    take: Annotated[str, AfterValidator(str_not_empty)]
    returns: Annotated[str, AfterValidator(str_not_empty)]  # Normally "return" but it clashes with python's return.
    change: Annotated[str, AfterValidator(str_not_empty)]


class StorySpine(StoryStructure):
    once_upon_a_time: Annotated[str, AfterValidator(str_not_empty)]
    and_every_day: Annotated[str, AfterValidator(str_not_empty)]
    until_one_day: Annotated[str, AfterValidator(str_not_empty)]
    and_because_of_this: Annotated[str, AfterValidator(str_not_empty)]
    and_then: Annotated[str, AfterValidator(str_not_empty)]
    until_finally: Annotated[str, AfterValidator(str_not_empty)]
    and_ever_since_that_day: Annotated[str, AfterValidator(str_not_empty)]


class FichteanCurveStructure(StoryStructure):
    inciting_incident: Annotated[str, AfterValidator(str_not_empty)]
    first_crisis: Annotated[str, AfterValidator(str_not_empty)]
    second_crisis: Annotated[str, AfterValidator(str_not_empty)]
    third_crisis: Annotated[str, AfterValidator(str_not_empty)]
    fourth_crisis: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]


class InMediasRes(StoryStructure):
    in_medias_res: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    explanation: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class SaveTheCatStructure(StoryStructure):
    opening_image: Annotated[str, AfterValidator(str_not_empty)]
    set_up: Annotated[str, AfterValidator(str_not_empty)]
    theme_stated: Annotated[str, AfterValidator(str_not_empty)]
    catalyst: Annotated[str, AfterValidator(str_not_empty)]
    debate: Annotated[str, AfterValidator(str_not_empty)]
    break_into_two: Annotated[str, AfterValidator(str_not_empty)]
    b_story: Annotated[str, AfterValidator(str_not_empty)]
    fun_and_games: Annotated[str, AfterValidator(str_not_empty)]
    midpoint: Annotated[str, AfterValidator(str_not_empty)]
    bad_guys_close_in: Annotated[str, AfterValidator(str_not_empty)]
    all_is_lost: Annotated[str, AfterValidator(str_not_empty)]
    dark_night_of_the_soul: Annotated[str, AfterValidator(str_not_empty)]
    break_into_three: Annotated[str, AfterValidator(str_not_empty)]
    finale: Annotated[str, AfterValidator(str_not_empty)]
    final_image: Annotated[str, AfterValidator(str_not_empty)]


# End of the Story Structure section


class GeneralData(CustomBaseModel):
    """
    A model to represent the general details of a outline as defined by the structured output of an LLM.
    This model must match the json schema of the LLM's response_format input.
    """

    title: Annotated[str, AfterValidator(str_not_empty)]
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
    def clean_arrays(cls, value):
        """
        Account for some of the weird ways the LLM outputs sometimes.

        Examples: ["Self-discovery | Friendship | Redemption"]
        """
        for item in value:
            if "|" in item:
                sub_values = item.split("|")
                value.remove(item)
                value.extend(sub_values)

        # Clean up any whitespace.
        for item in value:
            item.strip()

        return value


class StructureData(CustomBaseModel):
    style: str  # e.g. "Three-Act Structure"
    structure: (
        ClassicStoryStructure
        | ThreeActStructure
        | FiveActStructure
        | SevenPointStoryStructure
        | FreytagsPyramidStoryStructure
        | TheHerosJourneyStoryStructure
        | DanHarmonsStoryCircleStructure
        | StorySpine
        | FichteanCurveStructure
        | InMediasRes
        | SaveTheCatStructure
    )


class WorldbuildingData(CustomBaseModel):
    # Todo: Create a validator to validate that some of these fields are filled out.
    #  I don't think all of them have to be filled out for every story, but at least some should.
    geography: str | None = None
    culture: str | None = None
    history: str | None = None
    politics: str | None = None
    economy: str | None = None
    magic_technology: str | None = None
    religion: str | None = None
    additional_details: str | None = None


class CharacterData(CustomBaseModel):
    name: Annotated[str, AfterValidator(str_not_empty)]
    age: Annotated[str, AfterValidator(str_not_empty)]
    role: Annotated[str, AfterValidator(str_not_empty)]
    description: Annotated[str, AfterValidator(str_not_empty)]
    personality: Annotated[str, AfterValidator(str_not_empty)]

    def save_to_file(self, output_dir: Path, file_type: Literal["json", "yaml"], filename: str = None):
        super().save_to_file(output_dir=output_dir, file_type=file_type, filename=f"{self.name}")

    @classmethod
    def load_from_file(cls: type[CBM], file_type: Literal["json", "yaml"], file_path: Path) -> CBM:
        return super().load_from_file(file_path=file_path, file_type=file_type)


class ChapterCharacterData(CustomBaseModel):
    name: Annotated[str, AfterValidator(str_not_empty)]
    status: Annotated[str, AfterValidator(str_not_empty)]


class SceneData(CustomBaseModel):
    summary: Annotated[str, AfterValidator(str_not_empty)]
    number: int | None = None  # This is added manually. LLMs don't always count in order.
    characters: list[ChapterCharacterData]
    location: Annotated[str, AfterValidator(str_not_empty)]
    misc: str | None = None
    story_beats: list[Annotated[str, AfterValidator(str_not_empty)]]

    def save_to_file(self, output_dir: Path, file_type: Literal["json", "yaml"], filename: str = None):
        super().save_to_file(output_dir=output_dir, file_type=file_type, filename=filename)


class ChapterData(CustomBaseModel):
    title: Annotated[str, AfterValidator(str_not_empty)]
    number: int | None = None  # This is added manually. LLMs don't always count in order.
    story_structure_point: Annotated[str, AfterValidator(str_not_empty)]
    location: Annotated[str, AfterValidator(str_not_empty)]
    characters: list[ChapterCharacterData]
    synopsis: Annotated[str, AfterValidator(str_not_empty)]
    scenes: list[SceneData] = []

    def save_to_file(self, output_dir: Path, file_type: Literal["json", "yaml"], filename: str = None):
        """

        :param output_dir: This is the /chapterdata/ directory
        :param file_type: json or yaml, based on a user setting
        :param filename: None
        :return: None, creates a /Chapter-n/ directory and saves the chapter and scenes within that dir.
        """
        chapter_dir = output_dir / f"Chapter-{self.number}"
        chapter_dir.mkdir(exist_ok=True)
        super().save_to_file(output_dir=chapter_dir, file_type=file_type, filename=f"chapter-{self.number}")

        if self.scenes:
            for scene in self.scenes:
                scene.save_to_file(output_dir=chapter_dir, file_type=file_type, filename=f"scene-{self.number}")

    @classmethod
    def load_from_file(cls: type[CBM], file_type: Literal["json", "yaml"], file_path: Path) -> CBM:
        # Load chapter data
        print(f"chapter file path {file_path=}")
        chapter_file = file_path / f"chapter-{file_path.name.split('-')[-1]}.{file_type}"
        if file_type == "json":
            with open(chapter_file, encoding="utf-8") as f:
                chapter_data = json.load(f)
        elif file_type == "yaml":
            with open(chapter_file, encoding="utf-8") as f:
                chapter_data = yaml.safe_load(f)
        else:
            raise Exception(f"File type: '{file_type}' not supported.")

        scenes = []
        for scene_file in sorted(file_path.glob(f"scene-*.{file_type}")):
            print(f"{scene_file=}")
            scenes.append(SceneData.load_from_file(file_type=file_type, file_path=scene_file))

        chapter_data["scenes"] = scenes

        return cls(**chapter_data)


class StoryData(CustomBaseModel):
    general: GeneralData | None = None
    structure: StructureData | None = None
    worldbuilding: WorldbuildingData | None = None
    characters: list[CharacterData] | None = None
    chapters: list[ChapterData] | None = None

    def __str__(self):
        return f"{self.general.title}"

    def save_to_file(self, output_dir: Path, file_type: str, filename: str = None, one_file: bool = True):
        """
        Saves the StoryData output depending on a couple of settings.
        :param output_dir: Should be /stories/
        :param file_type: json or yaml, based on user setting.
        :param filename: None
        :param one_file: bool - If True, saves the StoryData data as one file: "story_data.*" Otherwise, save files separately
        :return:
        """
        # story_dir = output_dir / self.general.title
        story_dir = output_dir
        story_dir.mkdir(parents=True, exist_ok=True)

        if one_file:
            # Save the data into one file as either a json or yaml file.
            story_data_path = story_dir / f"story_data.{file_type}"
            log.debug(f"Saving/Updating outline data to {story_data_path}")

            if file_type == "yaml":
                with open(story_data_path, mode="w+", encoding="utf-8") as f:
                    yaml.dump(self.model_dump(mode="python"), f, default_flow_style=False, sort_keys=False)

            elif file_type == "json":
                with open(story_data_path, mode="w+", encoding="utf-8") as f:
                    json.dump(self.model_dump(mode="json"), f, indent=4, sort_keys=False)

            else:
                log.error(f"Failed to save story data, save type is invalid: {file_type}")

        else:
            # Save each property separately (dicts as files, lists as files within a directory)
            for key, value in self.model_dump(mode="python").items():
                if value is None:
                    continue  # Prevents creating empty files/folders

                if isinstance(value, list):
                    # Create the subdirectory for the list of x
                    list_dir = story_dir / key
                    list_dir.mkdir(exist_ok=True)
                    print(f"{value=}")
                    for character in self.__getattribute__(key):
                        print(f"{character=}")
                        character.save_to_file(output_dir=list_dir, file_type=file_type)

                elif isinstance(value, dict):
                    self.__getattribute__(key).save_to_file(
                        output_dir=story_dir, file_type=file_type, filename=f"{key}"
                    )

    @classmethod
    def load_from_file(
        cls: type[CBM], saved_dir: Path, file_type: Literal["json", "yaml"], one_file: bool = True
    ) -> "StoryData":
        if one_file:
            story_data_path = saved_dir / f"story_data.{file_type}"
            log.debug(f"Loading outline data from '{story_data_path}'")

            if file_type == "yaml":
                with open(story_data_path, encoding="utf-8") as f:
                    return StoryData(**yaml.safe_load(f))

            elif file_type == "json":
                with open(story_data_path, encoding="utf-8") as f:
                    return StoryData(**json.load(fp=f))
            else:
                log.error(f"Failed to load story data, save type is invalid: {file_type}")

        else:
            story_data = {}
            for key in ["general", "structure", "worldbuilding"]:
                file = saved_dir / f"{key}.{file_type}"
                if file.exists():
                    print(f"{key} {file=}")
                    story_data[key] = globals()[key.capitalize() + "Data"].load_from_file(
                        file_type=file_type, file_path=file
                    )

            char_dir = saved_dir / "characters"
            if char_dir.exists():
                characters = []
                for char_file in char_dir.glob("*.json"):
                    characters.append(CharacterData.load_from_file(file_type=file_type, file_path=char_file))
                story_data["characters"] = characters

            chapter_dir = saved_dir / "chapters"
            if chapter_dir.exists():
                chapters = []
                for chapter_subdir in sorted(chapter_dir.iterdir()):
                    if chapter_subdir.is_dir():
                        chapters.append(ChapterData.load_from_file(file_type=file_type, file_path=chapter_subdir))
                story_data["chapters"] = chapters

            return cls(**story_data)


if __name__ == "__main__":
    import yaml

    with open("../stories/Radioactive Whiskers - 1738030968435/story_data.yaml", encoding="utf-8") as f:
        story_data = StoryData(**yaml.safe_load(f))

    print(story_data)
