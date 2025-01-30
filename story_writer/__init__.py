import logging
from pathlib import Path

import yaml

from story_writer.story_config import Settings

console_handler = logging.StreamHandler()
# TODO: Add color to formatting? Tried "colorlog", doesn't seem to work for Windows. /shrug
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

with open(Path(__file__).parents[1] / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

settings = Settings(**config)
