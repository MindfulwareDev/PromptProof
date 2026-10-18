#!/usr/bin/env python3
"""
PromptProof Guard Combiner CLI

Combines multiple guard files into a single system prompt,
counts tokens, and warns if budget is exceeded.

Usage:
    python combine.py --guards safety/01 quality/10 transparency/16
    python combine.py --profile developer
    python combine.py --profile researcher --budget 2000
    python combine.py --list-guards
    python combine.py --list-profiles
"""

import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
GUARDS_DIR = os.path.join(REPO_ROOT, "guards")
PROFILES_DIR = os.path.join(REPO_ROOT, "profiles")

# Token budget presets (approximate system prompt limits)
BUDGET_PRESETS = {
    "small": 1000,
    "medium": 2000,
    "standard": 4000,
    "large": 8000,
    "xlarge": 16000,
}

# Rough token estimation: ~4 chars per token for English text
CHARS_PER_TOKEN = 4


def estimate_tokens(text):
    """Estimate token count using character-based heuristic."""
    return len(text) // CHARS_PER_TOKEN


def find_guard_file(query):
    """Find a guard file by partial name match."""
    # Restrict selection to this library, including symlink targets.
    root = Path(GUARDS_DIR).resolve()
    query = query[7:] if query.startswith("guards/") else query
    if not query or Path(query).is_absolute() or ".." in Path(query).parts:
        raise ValueError("Guard must be a name or relative path inside guards/")
    candidates = []
    for path in sorted(root.rglob("*.md")):
        if root not in path.resolve().parents:
            continue
        relative = path.relative_to(root).as_posix()
        if relative == query or relative == query + ".md":
            return str(path)
        category, _, fragment = query.rpartition("/")
        if category and path.parent.relative_to(root).as_posix() != category:
            continue
        if fragment.lower() in path.name.lower():
            candidates.append(str(path))
    if len(candidates) > 1:
        raise ValueError("Ambiguous guard: " + query + "; use a full relative path")
    return candidates[0] if candidates else None


def list_guards():
    """List all available guards."""
    categories = {}
    for root, dirs, files in os.walk(GUARDS_DIR):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            cat = os.path.basename(root)
            if cat not in categories:
                categories[cat] = []
            full = os.path.join(root, f)
            content = Path(full).read_text(encoding="utf-8")
            tokens = estimate_tokens(content)
            # Extract first heading as description
            first_line = ""
            for line in content.split("\n"):
                if line.startswith("# "):
                    first_line = line[2:].strip()
                    break
            categories[cat].append((f, first_line, tokens))

    for cat in sorted(categories.keys()):
        print(f"\n  {cat.upper()}")
        print(f"  {'─' * 60}")
        for name, desc, tokens in categories[cat]:
            print(f"    {name:<45} ~{tokens:>4} tokens")
    print()


def list_profiles():
    """List available profiles."""
    if not os.path.isdir(PROFILES_DIR):
        print("No profiles directory found.")
        return

    print("\n  AVAILABLE PROFILES")
    print(f"  {'─' * 60}")
    for f in sorted(os.listdir(PROFILES_DIR)):
        if not f.endswith(".txt") and not f.endswith(".md"):
            continue
        full = os.path.join(PROFILES_DIR, f)
        content = Path(full).read_text(encoding="utf-8")
        # Count guards listed
        guard_lines = [l for l in content.split("\n") if l.strip().startswith("guards/")]
        tokens = estimate_tokens(content)
        name = os.path.splitext(f)[0]
        print(f"    {name:<25} {len(guard_lines)} guards, ~{tokens:>4} tokens")
    print()


def load_profile(name):
    """Load guard list from a profile file."""
    if not name or Path(name).is_absolute() or len(Path(name).parts) != 1 or name in (".", ".."):
        raise ValueError("Profile must be a name inside profiles/")
    for ext in [".txt", ".md", ""]:
        path = os.path.join(PROFILES_DIR, name + ext)
        if os.path.isfile(path) and Path(PROFILES_DIR).resolve() in Path(path).resolve().parents:
            content = Path(path).read_text(encoding="utf-8")
            guards = []
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("guards/"):
                    guards.append(line)
                elif line.startswith("#") or line == "" or line.startswith("Profile:"):
                    continue
            return guards
    return None


def combine_guards(guard_paths, budget=None, output_file=None):
    """Combine guard files into a single system prompt."""
    # Resolve everything before writing so missing guards cannot yield a partial prompt.
    resolved_paths = []
    for query in guard_paths:
        resolved = find_guard_file(query)
        if resolved is None:
            raise ValueError("Guard not found: " + query)
        if resolved not in resolved_paths:
            resolved_paths.append(resolved)
    combined = []
    total_tokens = 0
    loaded = []

    header = (
        "# PromptProof Combined Guard System Prompt\n"
        "# Generated by PromptProof Guard Combiner\n"
        "# https://github.com/MindfulwareDev/PromptProof\n"
        "#\n"
        f"# Guards loaded: {len(resolved_paths)}\n"
        "\n"
    )
    combined.append(header)
    total_tokens += estimate_tokens(header)

    for resolved in resolved_paths:
        content = Path(resolved).read_text(encoding="utf-8")
        tokens = estimate_tokens(content)
        total_tokens += tokens

        rel_path = os.path.relpath(resolved, REPO_ROOT)
        loaded.append((rel_path, tokens))

        separator = f"\n# {'=' * 60}\n# Guard: {rel_path}\n# {'=' * 60}\n\n"
        combined.append(separator)
        combined.append(content)
        combined.append("\n")
        total_tokens += estimate_tokens(separator)

    result = "".join(combined)
    total_tokens = estimate_tokens(result)

    # Output
    print(f"\n  COMBINED SYSTEM PROMPT")
    print(f"  {'─' * 60}")
    for path, tokens in loaded:
        print(f"    + {path:<45} ~{tokens:>4} tokens")
    print(f"  {'─' * 60}")
    print(f"    TOTAL: ~{total_tokens} tokens")

    if budget:
        budget_val = BUDGET_PRESETS.get(budget, None)
        if budget_val is None:
            try:
                budget_val = int(budget)
            except ValueError:
                print(f"  WARNING: Invalid budget '{budget}'. Use a number or: {', '.join(BUDGET_PRESETS.keys())}")
                budget_val = None

        if budget_val:
            remaining = budget_val - total_tokens
            if remaining < 0:
                print(f"  ⚠ OVER BUDGET by ~{-remaining} tokens (budget: {budget_val})")
                print(f"    Consider removing a guard or using a larger budget.")
            else:
                print(f"    Budget: {budget_val} tokens | Remaining: ~{remaining} tokens")

    if output_file:
        with open(output_file, "w") as f:
            f.write(result)
        print(f"\n    Written to: {output_file}")
    else:
        print(f"\n    Use --output <file> to save, or pipe stdout:")
        print(f"    python combine.py --guards ... --raw > system_prompt.txt")

    print()
    return result


def main():
    parser = argparse.ArgumentParser(
        description="PromptProof Guard Combiner — build composite system prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine.py --list-guards
  python combine.py --list-profiles
  python combine.py --profile developer
  python combine.py --profile developer --budget 2000
  python combine.py --guards safety/01 quality/10 --output prompt.txt
  python combine.py --guards prompt-injection hallucination --budget standard
        """,
    )
    parser.add_argument("--guards", nargs="+", help="Guard files to combine (partial names ok)")
    parser.add_argument("--profile", help="Use a preset profile")
    parser.add_argument("--budget", help="Token budget (number or: small/medium/standard/large/xlarge)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--raw", action="store_true", help="Output raw combined prompt to stdout")
    parser.add_argument("--list-guards", action="store_true", help="List all available guards")
    parser.add_argument("--list-profiles", action="store_true", help="List all available profiles")

    args = parser.parse_args()

    if args.list_guards:
        list_guards()
        return

    if args.list_profiles:
        list_profiles()
        return

    guard_paths = []

    if args.profile:
        try:
            profile_guards = load_profile(args.profile)
        except ValueError as exc:
            parser.error(str(exc))
        if profile_guards is None:
            print(f"Profile not found: {args.profile}")
            print("Use --list-profiles to see available profiles.")
            sys.exit(1)
        guard_paths.extend(profile_guards)

    if args.guards:
        guard_paths.extend(args.guards)

    if not guard_paths:
        parser.print_help()
        sys.exit(1)

    from contextlib import redirect_stdout
    try:
        with redirect_stdout(sys.stderr if args.raw else sys.stdout):
            result = combine_guards(guard_paths, budget=args.budget, output_file=args.output)
    except ValueError as exc:
        parser.error(str(exc))

    if args.raw:
        print(result, end="")


if __name__ == "__main__":
    main()
