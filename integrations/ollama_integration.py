"""
PromptProof + Ollama Integration Template

Drop-in example for using PromptProof guards with local LLMs via Ollama.
No API key required — runs entirely on your machine.

Requirements:
    1. Install Ollama: https://ollama.ai
    2. Pull a model: ollama pull llama3
    3. Start Ollama: ollama serve

No pip dependencies required (uses urllib).
"""

import json
import os
import sys
import urllib.request
import urllib.error

# --- Configuration ---
MODEL = "llama3"  # or "mistral", "codellama", "phi3", etc.
OLLAMA_URL = "http://localhost:11434"

# Path to PromptProof repo root
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


def check_ollama():
    """Check if Ollama is running."""
    try:
        urllib.request.urlopen(OLLAMA_URL)
        return True
    except urllib.error.URLError:
        return False


def chat(user_message, system_prompt, conversation_history=None):
    """Send a message with PromptProof guards active."""
    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    data = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result["message"]["content"]


def chat_stream(user_message, system_prompt, conversation_history=None):
    """Send a message with streaming response."""
    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    data = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": True,
    }).encode()

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    full_response = []
    resp = urllib.request.urlopen(req)
    for line in resp:
        if line.strip():
            chunk = json.loads(line)
            if "message" in chunk and "content" in chunk["message"]:
                content = chunk["message"]["content"]
                full_response.append(content)
                print(content, end="", flush=True)
            if chunk.get("done", False):
                break

    print()
    return "".join(full_response)


# --- Example usage ---

if __name__ == "__main__":
    if not check_ollama():
        print("Ollama is not running. Start it with: ollama serve")
        print("Then pull a model: ollama pull llama3")
        sys.exit(1)

    # Load a profile
    system_prompt = load_profile("developer")

    print("PromptProof + Ollama (Local LLM) Demo")
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
