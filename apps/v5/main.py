# main.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic
import subprocess

# Load environment variables from .env file
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL")

SYSTEM_PROMPT = """
You are a helpful assistant who help user execute a task.
1. If the execution of command line is required, then output only one line of shell command
command: <executable_command>

2. If no further execution is required, then output in this format:
complete: <summary_text>

Keep the output concise.
""".strip()


def main() -> None:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # context
    context = []

    while True:
        user_input = input("\n>>User Input:\n")

        # append input to context
        context.append({"role": "user", "content": user_input})

        print("\n---------- Agent is thinking ----------")

        while True:

            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,  # add system prompt
                messages=context
            )

            # get output
            llm_output = response.content[0].text.strip()
            # save output into context
            context.append({"role": "assistant", "content": llm_output})

            # if complete: break loop
            if llm_output.startswith("complete:"):
                print(">>LLM Output:")
                print(llm_output.split("complete:", 1)[1].strip())

                break

            # if command: execute command
            elif llm_output.startswith("command:"):
                # get command
                print(">>LLM Output:")
                command = llm_output.split("command:", 1)[1].strip()
                print(command)

                # Exectute command
                print(
                    f"\n---------- Agent is exectuting command: {command} ----------")
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True)
                command_result = result.stdout + result.stderr
                exec_output = f"Execution completed: {command_result}"
                print(exec_output)

                # append the cli output for next loop
                context.append(
                    {"role": "user", "content": f"command execution: {exec_output}"})  # must be user role

            # guard
            else:
                context.append(
                    {"role": "user", "content": "Please follow the output format."})
                continue


if __name__ == "__main__":
    main()
