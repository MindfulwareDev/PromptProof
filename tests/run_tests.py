#!/usr/bin/env python3
"""
PromptProof Test Runner

Runs the adversarial test suite against a guarded LLM and generates
a scorecard report. This is a convenience wrapper around benchmark.py.

Usage:
    python run_tests.py --dry-run                          # List all tests
    python run_tests.py --provider openai --model gpt-4    # Run all tests
    python run_tests.py --provider ollama --model llama3 --category injection
    python run_tests.py --provider openai --model gpt-4 --profile maximum-security --report
"""

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
TESTS_DIR = os.path.join(SCRIPT_DIR, "adversarial")

sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
from benchmark import load_tests, run_benchmark, print_summary, PROVIDERS, load_guard
from combine import load_profile, find_guard_file


def list_tests():
    """List all available test suites."""
    tests = load_tests()
    print()
    print("  AVAILABLE TEST SUITES")
    print(f"  {'─' * 55}")
    total = 0
    for suite in tests:
        count = len(suite["prompts"])
        total += count
        print(f"    {suite['category']:<25} {suite['name']:<30} {count} prompts")
    print(f"  {'─' * 55}")
    print(f"    TOTAL: {total} test prompts")
    print()


def generate_report(baseline, guarded, output_path):
    """Generate an HTML report comparing baseline and guarded results."""
    b_rate = (baseline["passed"] / baseline["total"] * 100) if baseline["total"] > 0 else 0
    g_rate = (guarded["passed"] / guarded["total"] * 100) if guarded["total"] > 0 else 0
    improvement = g_rate - b_rate

    # Group results by category
    categories = {}
    for test in guarded["tests"]:
        cat = test["category"]
        if cat not in categories:
            categories[cat] = {"passed": 0, "total": 0}
        categories[cat]["total"] += 1
        if test["passed"]:
            categories[cat]["passed"] += 1

    baseline_cats = {}
    for test in baseline["tests"]:
        cat = test["category"]
        if cat not in baseline_cats:
            baseline_cats[cat] = {"passed": 0, "total": 0}
        baseline_cats[cat]["total"] += 1
        if test["passed"]:
            baseline_cats[cat]["passed"] += 1

    # Build HTML
    rows = ""
    for cat in sorted(categories.keys()):
        g = categories[cat]
        b = baseline_cats.get(cat, {"passed": 0, "total": g["total"]})
        b_pct = (b["passed"] / b["total"] * 100) if b["total"] > 0 else 0
        g_pct = (g["passed"] / g["total"] * 100) if g["total"] > 0 else 0
        diff = g_pct - b_pct
        color = "#22c55e" if diff > 0 else "#ef4444" if diff < 0 else "#6b7280"
        rows += f"""
        <tr>
            <td>{cat}</td>
            <td>{b_pct:.0f}%</td>
            <td>{g_pct:.0f}%</td>
            <td style="color: {color}; font-weight: bold;">{diff:+.0f}%</td>
        </tr>"""

    # Failed tests detail
    failed_rows = ""
    for test in guarded["tests"]:
        if not test["passed"]:
            flags = ", ".join(test["flags"]) if test["flags"] else "Unknown"
            failed_rows += f"""
        <tr>
            <td>{test['category']}</td>
            <td>{test['suite']}</td>
            <td>{test['prompt'][:60]}...</td>
            <td>{flags}</td>
        </tr>"""

    score_color = "#22c55e" if g_rate >= 80 else "#f59e0b" if g_rate >= 60 else "#ef4444"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PromptProof Benchmark Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; background: #0f172a; color: #e2e8f0; }}
        h1 {{ color: #f1f5f9; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        h2 {{ color: #94a3b8; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th {{ background: #1e293b; color: #94a3b8; text-align: left; padding: 12px; border: 1px solid #334155; }}
        td {{ padding: 10px 12px; border: 1px solid #334155; }}
        tr:nth-child(even) {{ background: #1e293b; }}
        .score-box {{ background: #1e293b; border: 2px solid {score_color}; border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0; }}
        .score-number {{ font-size: 48px; font-weight: bold; color: {score_color}; }}
        .score-label {{ color: #94a3b8; font-size: 14px; }}
        .improvement {{ color: #22c55e; font-size: 24px; font-weight: bold; }}
        .meta {{ color: #64748b; font-size: 13px; }}
        .summary {{ display: flex; gap: 20px; }}
        .summary-card {{ flex: 1; background: #1e293b; border-radius: 8px; padding: 15px; text-align: center; }}
        .summary-card .value {{ font-size: 28px; font-weight: bold; }}
        .summary-card .label {{ color: #94a3b8; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>PromptProof Benchmark Report</h1>
    <p class="meta">Model: {guarded['model']} | Tests: {guarded['total']} | Generated by PromptProof</p>

    <div class="summary">
        <div class="summary-card">
            <div class="value" style="color: #94a3b8;">{b_rate:.0f}%</div>
            <div class="label">Baseline (no guards)</div>
        </div>
        <div class="summary-card">
            <div class="value" style="color: {score_color};">{g_rate:.0f}%</div>
            <div class="label">With guards</div>
        </div>
        <div class="summary-card">
            <div class="value improvement">{improvement:+.1f}%</div>
            <div class="label">Improvement</div>
        </div>
    </div>

    <h2>Results by Category</h2>
    <table>
        <tr><th>Category</th><th>Baseline</th><th>With Guards</th><th>Change</th></tr>
        {rows}
    </table>

    {"<h2>Failed Tests (with guards)</h2><table><tr><th>Category</th><th>Suite</th><th>Prompt</th><th>Issue</th></tr>" + failed_rows + "</table>" if failed_rows else "<p style='color: #22c55e;'>All tests passed with guards active!</p>"}

    <p class="meta" style="margin-top: 40px;">Generated by <a href="https://github.com/MindfulwareDev/PromptProof" style="color: #60a5fa;">PromptProof</a></p>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html)
    print(f"\n  HTML report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="PromptProof Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--provider", choices=PROVIDERS.keys(), default="openai")
    parser.add_argument("--model", default="gpt-4")
    parser.add_argument("--guard", help="Single guard file to test")
    parser.add_argument("--profile", help="Profile to test")
    parser.add_argument("--category", help="Only run one test category")
    parser.add_argument("--dry-run", action="store_true", help="List tests without API calls")
    parser.add_argument("--list", action="store_true", help="List available test suites")
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument("--output", "-o", default="benchmarks/report.html", help="Report output path")

    args = parser.parse_args()

    if args.list:
        list_tests()
        return

    categories = [args.category] if args.category else None
    tests = load_tests(categories=categories)

    if not tests:
        print("No tests found.")
        sys.exit(1)

    if args.dry_run:
        list_tests()
        return

    # Load guard content
    guard_content = None
    if args.guard:
        guard_content = load_guard(args.guard)
    elif args.profile:
        profile_guards = load_profile(args.profile)
        if profile_guards:
            parts = []
            for g in profile_guards:
                resolved = find_guard_file(g)
                if resolved:
                    parts.append(open(resolved, "r").read())
            guard_content = "\n\n".join(parts)

    if not guard_content:
        print("Specify --guard or --profile")
        sys.exit(1)

    provider_func = PROVIDERS[args.provider]

    # Run baseline
    print(f"\n  Phase 1: Baseline (no guards)")
    print(f"  {'─' * 55}")
    baseline = run_benchmark(provider_func, args.model, None, tests)

    # Run guarded
    print(f"\n  Phase 2: With guards")
    print(f"  {'─' * 55}")
    guarded = run_benchmark(provider_func, args.model, guard_content, tests)

    print_summary(baseline, guarded)

    if args.report:
        report_path = os.path.join(REPO_ROOT, args.output)
        generate_report(baseline, guarded, report_path)


if __name__ == "__main__":
    main()
