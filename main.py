# import openai

from story_writer.tui.app import MainPageApp

if __name__ == '__main__':
    app = MainPageApp()
    app.run()

    # client = openai.Client(base_url="http://localhost:1234/v1", api_key="lm-studio")
    # response = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "Say this is a test."
    #         }
    #     ],
    #     model="llama-3.3-70b-instruct"
    # )
    # print(response)


    # import yaml
    # from pprint import pprint
    #
    # with open('../stories/The Arcane Spellbook/inputs/Chapters/chapter1.yaml') as f:
    #     try:
    #         pprint(yaml.safe_load(f))
    #     except yaml.YAMLError as err:
    #         pprint(err)
    #
    # with open('../stories/The Arcane Spellbook/inputs/characters.yaml') as f:
    #     try:
    #         pprint(yaml.safe_load(f))
    #     except yaml.YAMLError as err:
    #         pprint(err)
