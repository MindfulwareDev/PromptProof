"""
PromptProof + Anthropic (Claude) Integration Template

Drop-in example for using PromptProof guards with the Anthropic API.
Supports both streaming and non-streaming, with guard loading and combination.

Requirements:
    pip install anthropic

Set your API key:
    export ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import sys
import anthropic

# --- Configuration ---
MODEL = "claude-sonnet-4-20250514"  # or "claude-opus-4-20250514", "claude-haiku-4-5-20251001"

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
    client = anthropic.Anthropic()

    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=messages,
    )

    return response.content[0].text


def chat_stream(user_message, system_prompt, conversation_history=None):
    """Send a message with streaming response."""
    client = anthropic.Anthropic()

    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    full_response = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            full_response.append(text)
            print(text, end="", flush=True)

    print()
    return "".join(full_response)


# --- Example usage ---

if __name__ == "__main__":
    # Load a profile
    system_prompt = load_profile("researcher")

    print("PromptProof + Anthropic (Claude) Demo")
    print("=" * 40)
    print(f"Profile: researcher | Model: {MODEL}")
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
