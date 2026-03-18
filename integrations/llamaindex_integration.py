"""
PromptProof + LlamaIndex Integration Template

Shows how to use PromptProof guards with LlamaIndex for RAG pipelines.
Guards are injected as system prompts so all retrieved content is
processed through PromptProof's guardrails.

Requirements:
    pip install llama-index llama-index-llms-openai
    # or: pip install llama-index llama-index-llms-anthropic
    # or: pip install llama-index llama-index-llms-ollama
"""

import os

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.llms import ChatMessage, MessageRole

# --- Choose your provider (uncomment one) ---

# OpenAI
from llama_index.llms.openai import OpenAI
Settings.llm = OpenAI(model="gpt-4", temperature=0.7)

# Anthropic
# from llama_index.llms.anthropic import Anthropic
# Settings.llm = Anthropic(model="claude-sonnet-4-20250514")

# Ollama
# from llama_index.llms.ollama import Ollama
# Settings.llm = Ollama(model="llama3")

# --- PromptProof loader ---

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


def create_guarded_chat_engine(profile_name="developer"):
    """Create a LlamaIndex chat engine with PromptProof guards."""
    system_prompt = load_profile(profile_name)

    chat_engine = SimpleChatEngine.from_defaults(
        system_prompt=system_prompt,
    )

    return chat_engine


def create_guarded_rag_engine(documents_dir, profile_name="researcher"):
    """
    Create a RAG engine with PromptProof guards.
    Documents are indexed and queries are processed through guards.
    """
    system_prompt = load_profile(profile_name)

    # Load and index documents
    documents = SimpleDirectoryReader(documents_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)

    # Create query engine with guards as system prompt
    query_engine = index.as_chat_engine(
        system_prompt=system_prompt,
        chat_mode="condense_plus_context",
    )

    return query_engine


# --- Example usage ---

if __name__ == "__main__":
    # Option 1: Simple guarded chat (no RAG)
    print("PromptProof + LlamaIndex Demo (Chat)")
    print("=" * 40)

    chat_engine = create_guarded_chat_engine("researcher")

    response = chat_engine.chat("What are the main theories about dark matter?")
    print(f"Response: {response}")

    # Option 2: RAG with guards (uncomment and point to your docs)
    # print("\nPromptProof + LlamaIndex Demo (RAG)")
    # print("=" * 40)
    #
    # rag_engine = create_guarded_rag_engine("./my_documents", "researcher")
    # response = rag_engine.chat("Summarize the key findings from these documents.")
    # print(f"Response: {response}")
