from story_writer.cli import cli


if __name__ == "__main__":
    # Local urls may be "127.0.0.1" or "localhost"
    # LM Studio: http://url:1234/v1
    # Ollama:    http://url:11434/v1
    # Jan        http://url:1337/v1  < Doesn't support structured output as of 2025/01/27 (or so it seems)

    cli()
