# main.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL")

# providing context and instructions to LLM
SYSTEM_PROMPT = """
You are a helpful assistant.

Respond with this structure:
<format>:  <main_answer>

Field rules:
- "format": the most suitable output format
  - use "text" for normal answers; the default format.
  - use "command" only if the user explicitly asks for executable command.
- "main_answer": the main response to the user's request

Example: 
User: Who are you?
You: text I'm ...
User: What is the linux command to return the current working directory?
You: command pwd

Output rules:
- Keep "answer" concise and directly relevant to the user's request.
""".strip()


def main() -> None:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # context: a list to append
    context = []

    while True:
        user_input = input("\n>>User Input:\n")

        # append input to context
        context.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT, # add system prompt
            messages=context
        )
        # get output
        llm_output = response.content[0].text
        # append LLM output to context
        context.append({"role": "assistant", "content": llm_output})

        print(">>LLM Output:")
        print(llm_output)


if __name__ == "__main__":
    main()
