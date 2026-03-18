"""
PromptProof + LangChain Integration Template

Shows how to use PromptProof guards as system prompts in LangChain chains.
Works with any LangChain-supported LLM provider.

Requirements:
    pip install langchain langchain-openai
    # or: pip install langchain langchain-anthropic
    # or: pip install langchain langchain-ollama
"""

import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- Choose your provider (uncomment one) ---

# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Anthropic
# from langchain_anthropic import ChatAnthropic
# llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.7)

# Ollama (local)
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3", temperature=0.7)

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


def create_guarded_chain(profile_name="developer"):
    """Create a LangChain chain with PromptProof guards as system prompt."""
    system_prompt = load_profile(profile_name)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])

    chain = prompt | llm
    return chain


def create_guarded_chain_with_guards(*guard_paths):
    """Create a chain with specific guards instead of a profile."""
    guards = [load_guard(g) for g in guard_paths]
    system_prompt = "\n\n---\n\n".join(guards)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])

    chain = prompt | llm
    return chain


# --- Example usage ---

if __name__ == "__main__":
    # Option 1: Use a profile
    chain = create_guarded_chain("researcher")

    # Option 2: Use specific guards
    # chain = create_guarded_chain_with_guards(
    #     "guards/safety/01-prompt-injection-shield.md",
    #     "guards/quality/10-hallucination-tripwire.md",
    # )

    print("PromptProof + LangChain Demo")
    print("=" * 40)

    # Single invocation
    response = chain.invoke({"input": "What causes the northern lights?"})
    print(f"Response: {response.content}")

    # With conversation history
    print("\n--- With history ---")
    from langchain_core.messages import HumanMessage, AIMessage
    history = [
        HumanMessage(content="I'm researching climate change impacts on coral reefs."),
        AIMessage(content="I'll help with that research. What specific aspect are you focusing on?"),
    ]
    response = chain.invoke({
        "input": "What's the latest data on bleaching events?",
        "history": history,
    })
    print(f"Response: {response.content}")
