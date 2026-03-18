"""
PromptProof + OpenAI Integration Template

Drop-in example for using PromptProof guards with the OpenAI API.
Supports both streaming and non-streaming, with guard loading and combination.

Requirements:
    pip install openai

Set your API key:
    export OPENAI_API_KEY=sk-...
"""

import os
import sys
from openai import OpenAI

# --- Configuration ---
MODEL = "gpt-4"  # or "gpt-4o", "gpt-3.5-turbo", etc.

# Path to PromptProof repo root (adjust as needed)
PROMPTPROOF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_guard(guard_path):
    """Load a single guard file."""
    full_path = os.path.join(PROMPTPROOF_DIR, guard_path)
    with open(full_path, "r") as f:
        return f.read()


def load_profile(profile_name):
    """Load all guards from a profile and combine them."""
    profile_path = os.path.join(PROMPTPROOF_DIR, "profiles", f"{profile_name}.txt")
    with open(profile_path, "r") as f:
        lines = f.readlines()

    guards = []
    for line in lines:
        line = line.strip()
        if line.startswith("guards/"):
            guard_content = load_guard(line)
            guards.append(guard_content)

    return "\n\n---\n\n".join(guards)


def chat(user_message, system_prompt, conversation_history=None):
    """Send a message with PromptProof guards active."""
    client = OpenAI()

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content


def chat_stream(user_message, system_prompt, conversation_history=None):
    """Send a message with streaming response."""
    client = OpenAI()

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    full_response = []
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response.append(content)
            print(content, end="", flush=True)

    print()  # newline after stream
    return "".join(full_response)


# --- Example usage ---

if __name__ == "__main__":
    # Option 1: Load a single guard
    # system_prompt = load_guard("guards/safety/01-prompt-injection-shield.md")

    # Option 2: Load a full profile
    system_prompt = load_profile("developer")

    # Option 3: Combine specific guards manually
    # guards = [
    #     load_guard("guards/safety/01-prompt-injection-shield.md"),
    #     load_guard("guards/quality/10-hallucination-tripwire.md"),
    #     load_guard("guards/transparency/16-uncertainty-quantifier.md"),
    # ]
    # system_prompt = "\n\n---\n\n".join(guards)

    # Simple chat
    print("PromptProof + OpenAI Demo")
    print("=" * 40)
    print(f"Profile: developer | Model: {MODEL}")
    print(f"System prompt: ~{len(system_prompt) // 4} tokens")
    print("=" * 40)
    print()

    # Interactive loop
    history = []
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit"):
                break

            response = chat_stream(user_input, system_prompt, history)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            print()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
