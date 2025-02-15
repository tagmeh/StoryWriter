import logging

from openai import Client

from story_writer import settings
from story_writer.llm import get_validated_llm_output
from story_writer.models.outline import StoryData
from story_writer.models.outline_models import WorldbuildingData
from story_writer.prompts import generate_worldbuilding_prompt

log = logging.getLogger(__name__)


def generate_worldbuilding(client: Client):
    story_data: StoryData = StoryData.load_from_file(saved_dir=settings.story_dir)

    log.info(f"Generating Characters for story: '{story_data.general.title}'")

    instructions = generate_worldbuilding_prompt(story_data=story_data)
    messages = [
        {"role": "system", "content": settings.basic_system_prompt},
        {"role": "user", "content": instructions},
    ]

    # Todo: Potentially add a "character number check (too many or too few)" validator,
    #  if not, rerun validated_stream_llm
    content, elapsed = get_validated_llm_output(
        client=client,
        messages=messages,
        validation_model=WorldbuildingData,
        model_settings=settings.stage.worldbuilding,
        log_file_name="generate_worldbuilding",
    )

    story_data.worldbuilding = content

    story_data.save_to_file(output_dir=settings.story_dir)

    # Todo: Update the log_step function. Figure out what it's purpose is.
    #  Current issue is that the model used may differ depending on if a stage has a model set, or if it uses the default.
    #  Perhaps this is moved to the validated_llm output function, and the file_name is derived from the response_model.
    # utils.log_step(
    #     story_root=story_root,
    #     messages=messages,
    #     file_name="generate_worldbuilding",
    #     model=settings.llm.model,
    #     settings={},
    #     response_model=WorldbuildingData,
    #     duration=elapsed,
    # )
