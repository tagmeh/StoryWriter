import json
import logging
import re
from pathlib import Path
from typing import Annotated, Any, Literal, TypeVar, Type

import yaml
from pydantic import AfterValidator, BaseModel, field_validator, Field, TypeAdapter

from story_writer.constants import StoryStructureEnum

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
CBM = TypeVar("CBM", bound="CustomBaseModel")


def create_json_schema(model: Type[BaseModel]) -> dict[str, Any] | None:
    if model.__name__ in ['CharacterData', 'ChapterData', 'SceneData']:
        schema = TypeAdapter(list[model]).json_schema()
    else:
        schema = model.model_json_schema()
    return {
        "type": "json_schema",
        "json_schema": {
            "name": model.__name__,
            "strict": True,
            "schema": schema,
            "required": [model.__name__]
        }
    } if schema else None


def str_not_empty(value: str) -> str:
    """Prevents empty strings from being a valid input when requiring a string input."""
    value = value.strip()
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


class ClassicStoryStructure(StoryStructure):
    # Todo: Update the StoryStructure models to not output the style or description in the model json schema.
    style: str = "Classic Story Structure"
    description: str = "A generic outline structure for all types of stories."
    exposition: Annotated[str, AfterValidator(str_not_empty)]
    rising_action: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class ThreeActStructure(StoryStructure):
    style: str = "Three Act Structure"
    description: str = "Traditional outline structure, most structures follow a variation on this one. Very popular in movies"
    act_1_exposition: Annotated[str, AfterValidator(str_not_empty), Field(description="Establish the status quo.")]
    act_1_inciting_incident: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Event that starts the outline.")]
    act_1_plot_point_1: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist has decided to deal with the conflict.")]
    act_2_rising_action: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The hero is beset with various challenges that increase the stakes in the tension.")]
    act_2_midpoint: Annotated[str, AfterValidator(str_not_empty), Field(
        description="An event that turns everything on its head, nearly ruining the protagonist's chances of achieving their goal.")]
    act_2_plot_point_2: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Following the midpoint, the protagonist fails at a challenge. Protagonist may question capability of succeeding.")]
    act_3_pre_climax: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonist pulls themself together and prepares for the final confrontation.")]
    act_3_climax: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The final confrontation between the protagonist and antagonist. Protagonist usually wins.")]
    act_3_denouement: Annotated[str, AfterValidator(str_not_empty), Field(
        description="All loose ends are neatly tied up, consequences of the climax are clearly spelled out.")]


class FiveActStructure(StoryStructure):
    style: str = "Five Act Structure"
    description: str = "Basically the same as Freytag's Pyramid, but without the expectation of it being a tragedy."
    exposition: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Establish the status quo. Ends with the inciting incident.")]
    rising_action: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist pursues their goal as the stakes rise.")]
    climax: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Center of the outline, the point of no return.")]
    falling_action: Annotated[str, AfterValidator(str_not_empty), Field(
        description="We see the consequences of the climax. In a tragedy, things start to spiral out of control.")]
    resolution: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Everything is wrapped up. The protagonist is usually at their highest point.")]


class SevenPointStoryStructure(StoryStructure):
    style: str = "Seven Point Story Structure"
    description: str = ""
    hook: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_1: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_1: Annotated[str, AfterValidator(str_not_empty)]
    mid_point: Annotated[str, AfterValidator(str_not_empty)]
    pinch_point_2: Annotated[str, AfterValidator(str_not_empty)]
    plot_turn_2: Annotated[str, AfterValidator(str_not_empty)]
    resolution: Annotated[str, AfterValidator(str_not_empty)]


class FreytagsPyramidStoryStructure(StoryStructure):
    style: str = "Freytag's Pyramid"
    description: str = "A outline structure for tragic narratives."
    exposition: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Establish the status quo. Ends with the inciting incident.")]
    rising_action: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist pursues their goal as the stakes rise.")]
    climax: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Center of the outline, the point of no return.")]
    falling_action: Annotated[str, AfterValidator(str_not_empty), Field(
        description="We see the consequences of the climax. In a tragedy, things start to spiral out of control.")]
    denouement: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Everything is wrapped up. In a tragedy, the protagonist is at their lowest point.")]


class TheHerosJourneyStoryStructure(StoryStructure):
    style: str = "The Hero's Journey"
    description: str = "Campbell’s original structure uses terminology that lends itself well to epic tales of bravery and triumph."
    the_ordinary_world: Annotated[
        str, AfterValidator(str_not_empty), Field(description="The hero’s everyday life is established.")]
    the_call_to_adventure: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Otherwise known as the inciting incident.")]
    the_refusal_of_the_call: Annotated[str, AfterValidator(str_not_empty), Field(
        description="For a moment, the hero is reluctant to take on the challenge.")]
    meeting_the_mentor: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Our hero meets someone who prepares them for what lies ahead.")]
    crossing_the_threshold: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The hero steps out of their comfort zone and enters a ‘new world.’")]
    tests_allies_enemies: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Our protagonist faces new challenges, and maybe picks up some new friends.")]
    approach_to_the_inmost_cave: Annotated[
        str, AfterValidator(str_not_empty), Field(description="The hero gets close to their goal.")]
    the_ordeal: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The hero meets (and overcomes) their greatest challenge yet.")]
    seizing_the_sword: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The hero obtains something important they were after, and victory is in sight.")]
    the_road_back: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The hero realizes that achieving their goal is not the final hurdle.")]
    resurrection: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The hero faces their final challenge — a climactic test that hinges on everything they’ve learned over their journey.")]
    return_with_the_elixir: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Having triumphed, our protagonist returns to their old life. ")]


class DanHarmonsStoryCircleStructure(StoryStructure):
    style: str = "Dan Harmon's Story Circle"
    description: str = "A hero's journey type narrative that focuses more on character development."
    you: Annotated[str, AfterValidator(str_not_empty)]
    need: Annotated[str, AfterValidator(str_not_empty)]
    go: Annotated[str, AfterValidator(str_not_empty)]
    search: Annotated[str, AfterValidator(str_not_empty)]
    find: Annotated[str, AfterValidator(str_not_empty)]
    take: Annotated[str, AfterValidator(str_not_empty)]
    returns: Annotated[str, AfterValidator(str_not_empty)]  # Normally "return" but it clashes with python's return.
    change: Annotated[str, AfterValidator(str_not_empty)]


class StorySpine(StoryStructure):
    style: str = "Story Spine"
    description: str = ""
    once_upon_a_time: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Setup protagonist and the starting situation.")]
    and_every_day: Annotated[
        str, AfterValidator(str_not_empty), Field(description="More exposition, describing the status quo.")]
    until_one_day: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Inciting incident to shake things up.")]
    and_because_of_this: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonists are forced to leave their normal lives and go on an adventure.")]
    and_then: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The pursuit of their goals have consequences. A goal may have been achieved, but it leads to something else.")]
    until_finally: Annotated[str, AfterValidator(str_not_empty), Field(description="Climax of the outline.")]
    and_ever_since_that_day: Annotated[str, AfterValidator(str_not_empty), Field(
        description="How did the hero change from the journey. What did they bring back with them.")]


class FichteanCurveStructure(StoryStructure):
    style: str = "Fichtean Curve"
    description: str = "Packed with tension and mini-crises, the protagonist goes through multiple obstacles along their journey. Bypasses the 'ordinary world' setup."
    inciting_incident: Annotated[str, AfterValidator(str_not_empty)]
    first_crisis: Annotated[str, AfterValidator(str_not_empty)]
    second_crisis: Annotated[str, AfterValidator(str_not_empty)]
    third_crisis: Annotated[str, AfterValidator(str_not_empty)]
    fourth_crisis: Annotated[str, AfterValidator(str_not_empty)]
    climax: Annotated[str, AfterValidator(str_not_empty)]
    falling_action: Annotated[str, AfterValidator(str_not_empty)]


class InMediasRes(StoryStructure):
    style: str = "In Medias Res"
    description: str = "Framework for starting the outline in the middle of the action."
    in_medias_res: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Starts off immediately in the action with little to no exposition or backstory.")]
    rising_action: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Conflict increases, characters have to adjust. Still don't know everything going on at this time.")]
    explanation: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Rest point where exposition or backstory informs the reader what or why things are happening.")]
    climax: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Everything comes together and the protagonist succeeds or fails.")]
    falling_action: Annotated[str, AfterValidator(str_not_empty), Field(
        description="All loose ends are tied up and the reader is allowed to breathe.")]
    resolution: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonist returns to their ordinary world and plot threads are addressed.")]


class SaveTheCatStructure(StoryStructure):
    style: str = "Save the Cat"
    description: str = "A more detailed version of the three act structure."
    opening_image: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Story starts out with a brief look at the protagonist, gets the feel and tone of the outline.")]
    set_up: Annotated[str, AfterValidator(str_not_empty), Field(
        description="A little more exposition, setup the tone of the world, introduce the characters.")]
    theme_stated: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Make clear what the theme is. The theme may becomes more obvious to the progatonist as the outline progresses.")]
    catalyst: Annotated[
        str, AfterValidator(str_not_empty), Field(description="The inciting incident. The journey begins.")]
    debate: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonist fights or debates with the path they have taken.")]
    break_into_two: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Protagonist is fully invested in their quest.")]
    b_story: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Introduced to the b plot of the outline.")]
    fun_and_games: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonist enjoys a small amount of time to enjoy their new life, world, and abilities they have gained.")]
    midpoint: Annotated[
        str, AfterValidator(str_not_empty), Field(description="Something happens to turn the everything on its head.")]
    bad_guys_close_in: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The antagonist's forces become a greater threat to the protagonist.")]
    all_is_lost: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Something happens to the protagonist and puts them under extreme duress. ")]
    dark_night_of_the_soul: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The protagonist goes through a depressive period when it seems all hope is lost.")]
    break_into_three: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonist rises up from rock bottom and gains a key piece of knowledge that helps them in the future.")]
    finale: Annotated[str, AfterValidator(str_not_empty), Field(
        description="Protagonist takes what they have learned from their journey to defeat the antagonist.")]
    final_image: Annotated[str, AfterValidator(str_not_empty), Field(
        description="The final snapshot of the outline, it should mirror the opening image.")]


# End of the Story Structure section


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

    def __iter__(self):
        return iter(self)

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

        # TODO: Know that the scenes are still saved with the chapter.
        #  Possible way of going about it, solution?, is to save the scenes then clear them from the chapter,
        #  maybe with a message indicating the files are saved separately.
        chapter_data["scenes"] = scenes

        return cls(**chapter_data)


class StoryData(CustomBaseModel):
    general: GeneralData | None = None
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
            | None
    ) = None
    worldbuilding: WorldbuildingData | None = None
    characters: list[CharacterData] | None = None
    chapters: list[ChapterData] | None = None

    def __str__(self):
        return f"{self.general.title}"

    def save_to_file(self, output_dir: Path,
                     file_type: Literal["json", "yaml"] = 'yaml',
                     one_file: bool = True,
                     filename: str = None):
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

        # if one_file:
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

        # else:
        #     # Save each property separately (dicts as files, lists as files within a directory)
        #     for key, value in self.model_dump(mode="python").items():
        #         if value is None:
        #             continue  # Prevents creating empty files/folders
        #
        #         if isinstance(value, list):
        #             # Create the subdirectory for the list of x
        #             list_dir = story_dir / key
        #             list_dir.mkdir(exist_ok=True)
        #             print(f"{value=}")
        #             for character in self.__getattribute__(key):
        #                 print(f"{character=}")
        #                 character.save_to_file(output_dir=list_dir, file_type=file_type)
        #
        #         elif isinstance(value, dict):
        #             self.__getattribute__(key).save_to_file(
        #                 output_dir=story_dir, file_type=file_type, filename=f"{key}"
        #             )

    # TODO: The load feature needs to do one of two things:
    #  1) Try to load the data both ways (consolidated/Not consolidated) because the style of saving can change between stories.
    #  2) Save a settings.json or similar for each story, then reference that to determine style of saving, file_type, ect.
    @classmethod
    def load_from_file(
            cls: type[CBM],
            saved_dir: Path,
            file_type: Literal["json", "yaml"] = 'yaml',
            one_file: bool = True
    ) -> "StoryData":
        # if one_file:
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

        # else:
        #     story_data = {}
        #     for key in ["general", "structure", "worldbuilding"]:
        #         file = saved_dir / f"{key}.{file_type}"
        #         if file.exists():
        #             print(f"{key} {file=}")
        #             story_data[key] = globals()[key.capitalize() + "Data"].load_from_file(
        #                 file_type=file_type, file_path=file
        #             )
        #
        #     char_dir = saved_dir / "characters"
        #     if char_dir.exists():
        #         characters = []
        #         for char_file in char_dir.glob("*.json"):
        #             characters.append(CharacterData.load_from_file(file_type=file_type, file_path=char_file))
        #         story_data["characters"] = characters
        #
        #     chapter_dir = saved_dir / "chapters"
        #     if chapter_dir.exists():
        #         chapters = []
        #         for chapter_subdir in sorted(chapter_dir.iterdir()):
        #             if chapter_subdir.is_dir():
        #                 chapters.append(ChapterData.load_from_file(file_type=file_type, file_path=chapter_subdir))
        #         story_data["chapters"] = chapters
        #
        #     return cls(**story_data)


STORY_STYLE_MODEL_MAPPING = {
    StoryStructureEnum.CLASSIC: ClassicStoryStructure,
    StoryStructureEnum.THREE_ACT_STRUCTURE: ThreeActStructure,
    StoryStructureEnum.FIVE_ACT_STRUCTURE: FiveActStructure,
    StoryStructureEnum.SEVEN_POINT: SevenPointStoryStructure,
    StoryStructureEnum.FREYTAGS_PYRAMID: FreytagsPyramidStoryStructure,
    StoryStructureEnum.THE_HEROS_JOURNEY: TheHerosJourneyStoryStructure,
    StoryStructureEnum.DAN_HARMONS_STORY_CIRCLE: DanHarmonsStoryCircleStructure,
    StoryStructureEnum.STORY_SPINE: StorySpine,
    StoryStructureEnum.FICHTEAN_CURVE: FichteanCurveStructure,
    StoryStructureEnum.IN_MEDIAS_RES: InMediasRes,
    StoryStructureEnum.SAVE_THE_CAT: SaveTheCatStructure
}