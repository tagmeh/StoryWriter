from openai import OpenAI
import argparse

from story_writer.scripts.generate_story_outline import generate_story_outline


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        type=str,
        default="1234",
    )
    parser.add_argument("--host", type=str, default="http://127.0.0.1")
    parser.add_argument("--api-key", type=str, default="story-writer")

    args = parser.parse_args()
    client = OpenAI(base_url=f"{args.host}:{args.port}/v1", api_key=args.api_key)

    with open("stories/prompt.txt", encoding="utf-8") as f:
        prompt = f.read()

    generate_story_outline(client, prompt.strip())
