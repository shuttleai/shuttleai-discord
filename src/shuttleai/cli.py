# import asyncclick as click
# import os

# class Messages:
#     def __init__(self):
#         self.messages = []

#     def add_message(self, content, role="user"):
#         self.messages.append({
#             "content": content,
#             "role": role
#         })

#     def clear(self):
#         self.messages = []

# messages = Messages()

# @click.group()
# def shuttleai_cli():
#     pass

# @shuttleai_cli.command()
# @click.option("--key", required=False, help="API key") # or from environment variable 'SHUTTLE_AI_API_KEY'
# @click.option('--model', required=False, help='Model name') # default to 'shuttle-turbo'
# @click.option('--input', required=True, help='Input text')
# @click.option('--stream', is_flag=True, help='Stream mode')
# async def chat(key, model, input, stream):
#     key = key or os.environ.get('SHUTTLE_AI_API_KEY') or click.prompt('[Warning]: The `SHUTTLE_AI_API_KEY` environment variable is not set]\nPlease enter your API key', hide_input=True)
#     model = model or 'shuttle-turbo'

#     messages.add_message(input)


# if __name__ == '__main__':
#     shuttleai_cli()