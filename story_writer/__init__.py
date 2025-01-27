import logging

console_handler = logging.StreamHandler()
# TODO: Add color to formatting? Tried "colorlog", doesn't seem to work for Windows. /shrug
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
