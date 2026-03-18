#!/usr/bin/env python3
"""
PromptProof Prompt Linter

Analyzes any system prompt for common weaknesses and missing guardrails.
Produces a scored report with specific recommendations.

Usage:
    python lint_prompt.py path/to/system_prompt.txt
    python lint_prompt.py --stdin < prompt.txt
    echo "You are a helpful assistant." | python lint_prompt.py --stdin
"""

import argparse
import os
import sys
import re
import json

# Each check returns (passed: bool, severity: str, message: str, recommendation: str)
# Severity: CRITICAL, HIGH, MEDIUM, LOW, INFO


def check_injection_protection(text):
    """Check for prompt injection defenses."""
    keywords = [
        "injection", "override", "ignore previous", "jailbreak",
        "instruction", "immutable", "system prompt"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "CRITICAL",
        "Prompt injection protection",
        "Add instructions to reject override attempts. See guards/safety/01-prompt-injection-shield.md"
    )


def check_hallucination_control(text):
    """Check for hallucination mitigation."""
    keywords = [
        "hallucin", "verify", "unverified", "speculation", "confidence",
        "cite", "source", "fabricat", "[Inference]", "[Unverified]"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "HIGH",
        "Hallucination controls",
        "Add uncertainty labeling and confidence scoring. See guards/quality/10-hallucination-tripwire.md"
    )


def check_pii_protection(text):
    """Check for PII handling instructions."""
    keywords = [
        "pii", "personal", "identif", "redact", "privacy",
        "ssn", "email address", "phone number"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "HIGH",
        "PII protection",
        "Add PII detection and redaction rules. See guards/safety/02-pii-redactor.md"
    )


def check_disclaimer_presence(text):
    """Check for domain-specific disclaimers."""
    keywords = [
        "disclaimer", "not medical advice", "not legal advice",
        "not financial advice", "consult a professional", "qualified"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "MEDIUM",
        "Domain disclaimers",
        "Add disclaimers for high-risk domains (medical, legal, financial). See guards/domain/"
    )


def check_bias_awareness(text):
    """Check for bias detection."""
    keywords = [
        "bias", "fairness", "diverse", "perspective", "cultural",
        "assumption", "stereotype"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "MEDIUM",
        "Bias awareness",
        "Add bias detection and disclosure. See guards/quality/09-bias-detector.md"
    )


def check_output_structure(text):
    """Check for output formatting instructions."""
    keywords = [
        "format", "structure", "json", "markdown", "heading",
        "bullet", "list", "table"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "LOW",
        "Output structure",
        "Add output formatting guidelines. See guards/output/44-structured-output-enforcer.md"
    )


def check_refusal_protocol(text):
    """Check for graceful refusal instructions."""
    keywords = [
        "refuse", "decline", "cannot", "alternative", "instead",
        "not able", "won't"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "MEDIUM",
        "Refusal protocol",
        "Add graceful refusal with alternatives. See guards/behavioral/29-refusal-grace-protocol.md"
    )


def check_secret_protection(text):
    """Check for system prompt confidentiality."""
    keywords = [
        "confidential", "secret", "do not reveal", "do not disclose",
        "system prompt", "instructions are"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "HIGH",
        "System prompt confidentiality",
        "Add instructions to prevent prompt disclosure. See guards/safety/05-secret-keeper.md"
    )


def check_temporal_awareness(text):
    """Check for training data cutoff awareness."""
    keywords = [
        "cutoff", "training data", "current events", "outdated",
        "up to date", "real-time", "recent"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "MEDIUM",
        "Temporal awareness",
        "Add training cutoff disclosure. See guards/quality/14-temporal-awareness-guard.md"
    )


def check_code_safety(text):
    """Check for code generation safety rules."""
    keywords = [
        "code safety", "sql injection", "xss", "eval()", "exec(",
        "hardcoded", "credentials", "sanitiz"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "MEDIUM",
        "Code generation safety",
        "Add code safety rules. See guards/safety/06-code-execution-sandbox.md"
    )


def check_sycophancy_resistance(text):
    """Check for anti-sycophancy instructions."""
    keywords = [
        "disagree", "correct the user", "sycophancy", "honest",
        "don't just agree", "pushback", "accurate over"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "LOW",
        "Sycophancy resistance",
        "Add anti-sycophancy rules. See guards/behavioral/30-sycophancy-blocker.md"
    )


def check_crisis_handling(text):
    """Check for crisis/emergency handling."""
    keywords = [
        "crisis", "emergency", "suicide", "988", "hotline",
        "immediate danger", "self-harm"
    ]
    found = any(k.lower() in text.lower() for k in keywords)
    return (
        found,
        "HIGH",
        "Crisis handling",
        "Add crisis detection and resource provision. See guards/behavioral/31-emotional-regulation-guard.md"
    )


def check_prompt_length(text):
    """Check if prompt is suspiciously short."""
    tokens = len(text) // 4
    passed = tokens >= 50
    return (
        passed,
        "INFO",
        f"Prompt length (~{tokens} tokens)",
        "Very short prompts typically lack sufficient guardrails. Consider adding more specific instructions."
    )


def check_absolute_language(text):
    """Check for dangerous absolute language."""
    patterns = [
        r"\balways\s+comply\b",
        r"\bnever\s+refuse\b",
        r"\bdo\s+anything\b",
        r"\bno\s+restrictions\b",
        r"\bno\s+limits\b",
        r"\bunlimited\b",
    ]
    found_any = False
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            found_any = True
            break
    return (
        not found_any,
        "CRITICAL",
        "Dangerous absolute language",
        "Remove unrestricted compliance language. Phrases like 'always comply' or 'no restrictions' create safety vulnerabilities."
    )


ALL_CHECKS = [
    check_injection_protection,
    check_hallucination_control,
    check_pii_protection,
    check_secret_protection,
    check_crisis_handling,
    check_disclaimer_presence,
    check_bias_awareness,
    check_refusal_protocol,
    check_temporal_awareness,
    check_code_safety,
    check_sycophancy_resistance,
    check_output_structure,
    check_prompt_length,
    check_absolute_language,
]

SEVERITY_WEIGHT = {
    "CRITICAL": 20,
    "HIGH": 15,
    "MEDIUM": 10,
    "LOW": 5,
    "INFO": 2,
}

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


def lint_prompt(text):
    """Run all checks and produce a report."""
    results = []
    for check in ALL_CHECKS:
        passed, severity, name, recommendation = check(text)
        results.append({
            "passed": passed,
            "severity": severity,
            "name": name,
            "recommendation": recommendation,
        })
    return results


def calculate_score(results):
    """Calculate overall security score (0-100)."""
    max_score = sum(SEVERITY_WEIGHT[r["severity"]] for r in results)
    earned = sum(SEVERITY_WEIGHT[r["severity"]] for r in results if r["passed"])
    if max_score == 0:
        return 100
    return round((earned / max_score) * 100)


def print_report(results, score, text):
    """Print a formatted lint report."""
    tokens = len(text) // 4

    print()
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║           PROMPTPROOF PROMPT LINT REPORT                ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print()
    print(f"  Prompt size: ~{tokens} tokens ({len(text)} characters)")
    print(f"  Checks run: {len(results)}")
    print(f"  Passed: {sum(1 for r in results if r['passed'])}/{len(results)}")
    print()

    # Score bar
    bar_width = 40
    filled = round(score / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    if score >= 80:
        grade = "STRONG"
    elif score >= 60:
        grade = "MODERATE"
    elif score >= 40:
        grade = "WEAK"
    else:
        grade = "VULNERABLE"
    print(f"  Security Score: [{bar}] {score}/100 ({grade})")
    print()

    # Failed checks by severity
    failed = [r for r in results if not r["passed"]]
    if failed:
        print("  ISSUES FOUND:")
        print(f"  {'─' * 58}")
        for severity in SEVERITY_ORDER:
            sev_results = [r for r in failed if r["severity"] == severity]
            for r in sev_results:
                marker = "✗"
                print(f"    {marker} [{r['severity']}] {r['name']}")
                print(f"      → {r['recommendation']}")
                print()

    # Passed checks
    passed = [r for r in results if r["passed"]]
    if passed:
        print("  PASSING CHECKS:")
        print(f"  {'─' * 58}")
        for r in passed:
            print(f"    ✓ {r['name']}")
        print()

    return score


def json_report(results, score, text):
    """Generate JSON report."""
    return json.dumps({
        "score": score,
        "grade": "STRONG" if score >= 80 else "MODERATE" if score >= 60 else "WEAK" if score >= 40 else "VULNERABLE",
        "prompt_tokens": len(text) // 4,
        "checks_total": len(results),
        "checks_passed": sum(1 for r in results if r["passed"]),
        "results": results,
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="PromptProof Prompt Linter — analyze system prompts for weaknesses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python lint_prompt.py my_system_prompt.txt
  python lint_prompt.py --stdin < prompt.txt
  echo "You are a helpful assistant." | python lint_prompt.py --stdin
  python lint_prompt.py prompt.txt --json > report.json
        """,
    )
    parser.add_argument("file", nargs="?", help="Path to system prompt file")
    parser.add_argument("--stdin", action="store_true", help="Read prompt from stdin")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        text = open(args.file, "r").read()
    else:
        parser.print_help()
        sys.exit(1)

    if not text.strip():
        print("Empty prompt provided.", file=sys.stderr)
        sys.exit(1)

    results = lint_prompt(text)
    score = calculate_score(results)

    if args.json:
        print(json_report(results, score, text))
    else:
        print_report(results, score, text)

    # Exit code: 0 if score >= 60, 1 if below
    sys.exit(0 if score >= 60 else 1)


if __name__ == "__main__":
    main()
