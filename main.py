from openai import OpenAI

from story_writer.scripts.generate_story_outline import generate_story_outline

if __name__ == "__main__":
    # Local urls may be "127.0.0.1" or "localhost"
    # LM Studio: http://url:1234/v1
    # Ollama:    http://url:11434/v1
    # Jan        http://url:1337/v1  < Doesn't support structured output as of 2025/01/27 (or so it seems)
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm studio")

    with open("stories/prompt.txt", encoding="utf-8") as f:
        prompt = f.read()

    generate_story_outline(client, prompt.strip())
