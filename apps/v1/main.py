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

    user_input = "What is the capital of France?"
    # get LLM output
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    print("\n>>User Input:")
    print(user_input)

    print("\n>>LLM Output:")
    print(response.content[0].text)


if __name__ == "__main__":
    main()
