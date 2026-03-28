# main.py
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL")

# Paths relative
AGENT_DIR = Path(__file__).parent
AGENT_MD = AGENT_DIR / "AGENT.md"
SKILLS_DIR = AGENT_DIR / "skills"

# Load AGENT.md
with open(AGENT_MD, "r", encoding="utf-8") as f:
    AGENT_PROMPT = f.read()

SYSTEM_PROMPT = AGENT_PROMPT


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

            llm_output = response.content[0].text.strip()
            # save output into context
            context.append({"role": "assistant", "content": llm_output})

            # if complete: break loop
            if llm_output.startswith("complete:"):
                print(">>LLM Output:")
                print(llm_output.split("complete:", 1)[1].strip())

                break

            # if command: load skills
            elif llm_output.startswith("skill:"):
                # get command
                print(">>LLM Output:")
                skill_command = llm_output.split("skill:", 1)[1].strip()
                print(skill_command)

                # skills command
                print(
                    f"\n---------- Agent is load skill: {skill_command} ----------")
                result = subprocess.run(
                    skill_command, shell=True, capture_output=True, text=True)
                command_result = result.stdout + result.stderr
                skill_output = f"Load completed {command_result}"
                print(skill_output)
                # append the loaded skill for next loop
                context.append(
                    {"role": "user", "content": f"command execution: {skill_output}"})  # must be user role

            # if command: execute command
            elif llm_output.startswith("command:"):
                # get command
                print(">>LLM Output:")
                exec_command = llm_output.split("command:", 1)[1].strip()
                print(exec_command)

                # Exectute command
                print(
                    f"\n---------- Agent is exectuting command: {exec_command} ----------")
                result = subprocess.run(
                    exec_command, shell=True, capture_output=True, text=True)
                command_result = result.stdout + result.stderr
                exec_output = f"Execution completed {command_result}"
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
