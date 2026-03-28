# main.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL")


def main() -> None:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # context: a list to append
    context = []

    while True:
        user_input = input("\n>>User Input:\n")

        # append user input to context
        context.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
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
