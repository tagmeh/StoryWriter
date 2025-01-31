## This page is still under heavy editing. 

# StoryWriter

StoryWriter's goal is to generate a full story, given an initial prompt. The script uses a multi-stage approach, where the user can configure the LLM model settings for each stage independently. Once the script runs through each stage and has generated the outline, the user can review/edit the outline as they see fit. Then the process continues with a rough draft, again with user-configurable settings. Then, depending on what the user wants, multiple additional passes can be made to refine the output, adding detail, flowery language, dialogue. 

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
- [Usage](#usage)
    * [`prompt.txt` Configuration File](#prompptxt-configuration-file)
    * [`config.yaml` LLM Settings Configurations](#confiyaml-lm-settings-configurations)

## Features

While this script will output a story, it will only be as good as the model used. 
Each stage in the outline, rough draft, and subsequent editorial passes have user-define settings. You can use more logical models for the story structure outline phase, and a more creative model for the rough draft. You can set the system prompt for the dialogue stage to tweak how dialogue is inserted into the story.

1. **Edit `prompt.txt`**: Easily edit the story prompt located at `/stories/`.
2. **LLM Model Configuration**:
    * Configure different LLM models for each stage.
3. **Stage-wise Generation** (e.g., "General Story Data",  "Story Structure", etc.)
4. **Character Creation**
5. **Worldbuilding**: Define cultures, religions and geography
6. **Chapter Outline with Scenes**

## Getting Started
- User edits the `/stories/prompt.txt` creating a premise for a story.
- User updates the `config.yaml` settings file. The only required setting is the model name being used. However, the settings default to a local LM Studio instance. You can edit this in the `config.yaml`. An example file is included in the repository.
- Run main.py

## Script Process
1. Generates some general data. Ie. Title, Genres, Themes, and an expanded synoposis.
2. Given the user-definable Story Structure option, generates each step in the story structure. (Things like Three Act Story, Dan Harmon's Story Circle, Freytag's Pyramid, ex)

## Settings

### Story Structures
***Disclaimer Some of these story structures do poorly in an LLM, particularly Dan Harmon's Story Circle. As it was defined when I found it, each stage was named with a single word. Smaller models just return the next closest word to the story step, which doesn't make for a good story.***

List of story structures
- **Classic**: 
- **Dan Harmon's Story Circle**:
- **Fichtean Curve**:
- **Five Act**
- **Freytag's Pyramid**
- **In Medias Res**
- **Save The Cat**
- **Seven Point**
- **Story Spine**
- **The Hero's Journey**
- **Three Act** 

## Installation


### Prerequisites

Before you begin, ensure that you have the following installed:
- Python (version X.X or above)
- Required dependencies: [List of Dependencies]

To install required packages:

```bash
pip3 install -r requirements.txt  # Update this command as needed.
```

## Usage

The StoryWriter script allows users to generate a complete story outline and narrative by configuring two key files:
### `prompt.txt` Configuration File

Located at `/stories/`, edit the prompt file for initial storytelling prompts.

Example:

```text
Title: My Epic Adventure
Genre(s): Fantasy, Action
Theme(S):
Synopsis: A hero's journey through a magical land.
```

### `config.yaml` LLM Settings Configurations


This YAML configuration is used to define various settings and parameters required by the Large Language Models (LLMs):

```yaml

llm_model:
  default_settings:

    # Default fallback model configurations
      name: "default-model"
      api_key: 'your_api_key_here'
        endpoint_url : 'https://api.example.com'

# Model Settings for each stage of story generation.
general_data_creation :
     llm_name:"model-for-general-data"

story_structure:
   # Add configuration specific to this model and setting
```

### Supported Platforms

StoryWriter supports the following LLM platforms:

* Ollama
* ChatGPT (OpenAI)
* LM Studio

## License

This project is licensed under MIT.

---

Feel free to contribute, report issues or suggest new features. Happy writing!

## Todo:
- [ ] Capture and log usage data when using LM Studio
  - Review current data capture and improve on the implementation and data logging.
- [ ] Add option to save Outline data as yaml or json.
- [ ] Add option to save Outline as one file or separate files (for easier manual editing.)
- [ ] Update the Character model in the Outline to better capture the character's motivation, status, other details. Per chapter and per scene.

- [ ] Might try to create a graphical or textual interface.
- [ ] And of course, the various TODOs I have within the code =D.