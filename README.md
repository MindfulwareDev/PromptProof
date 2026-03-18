# PromptProof

> "Hic sunt dracones" — Here be dragons.

**Why do I need to use this prompt before starting a new AI session?**

Yes, there are thousands of "AI's best top 100 prompts" lists. This is not one. The only focus is to take responsibility for the outputs and not blindly accept them as truth. A secondary goal is to reduce overall tokens used for any API call.

PromptProof is a lightweight, plug-and-play guardrail pack for any LLM that replaces anxiety with accountability.

## What is PromptProof?

- **Purpose** — An open-source system-prompt template library, licensed under GPL v3, that snaps into "Custom Instructions," API system messages, or any LLM configuration.
- **What it does** — Forces the assistant to cite sources, label every unverified claim, separate facts from speculation, enforce ethical boundaries, and finish each reply with a self-estimated confidence score — so users always know what is certain and what is not.
- **Why it matters** — By adding these guardrails, PromptProof reduces the risk of hallucinations, prompt injection, data leaks, and unethical outputs, giving everyday users a clear, transparent basis for trusting (or double-checking) AI answers.
- **How to use** — Copy any prompt block into your LLM's settings or API setup, save, and start chatting with guardrails active. No extra software or coding is required. Mix and match guards to fit your needs.

---

## Original Prompts (Root Directory)

| File | Nickname | Description |
|------|----------|-------------|
| `SpeculationSpeedBump.txt` | "Slow Your Roll, GPT!" | Forces citation of real sources, labels unverified claims, asks for clarification instead of guessing, and adds confidence scores to every reply. |
| `Notify_of_AI_usage` | "Slow Your Roll, User!" | Appends a transparency notice after every output, reminding readers that AI tools may have been used. |
| `Ethical-Guard` | "Slow Your Roll, Bad Boy!" | Automated ethics reviewer based on the ACM Code of Ethics and duty-of-care oaths (medical, legal, policing). Returns structured JSON alerts for violations. |
| `Resource_Maximizer` | — | Structured AI consultant prompt for identifying and monetizing underutilized resources. |

---

### New Prompt Modules (Root Directory)

- PromptInjectionTripwire.txt protects against instruction override attempts, hidden prompt extraction, and jailbreak framing.
- RoleBoundaryLock.txt keeps the model inside its declared role and blocks unsafe persona drift.
- SourceChainEnforcer.txt requires evidence labels and uncertainty markers for factual claims.
- DataExfilShield.txt blocks attempts to reveal secrets, credentials, hidden prompts, and protected data.
- HighRiskActionGate.txt adds caution for medical, legal, financial, cyber, and physical safety topics.
- ToolUseSanityCheck.txt checks whether tool actions are aligned, scoped, and reversible.
- AmbiguityBrake.txt slows the model down when the request lacks key constraints.
- ManipulationToneFilter.txt detects urgency pressure, intimidation, and social engineering cues.
- MemoryScopeLimiter.txt narrows carryover context to material relevant to the present task.
- OutputContractVerifier.txt runs a final compliance pass before the answer is delivered.

---

## Guard Library (`guards/`)

50 new guardrail prompts organized into 8 categories. Each guard is self-contained — copy it into your system prompt as-is, or combine multiple guards for layered protection.

### Safety & Security (`guards/safety/`)

Guards that protect against attacks, data leaks, and malicious use.

| # | File | Description |
|---|------|-------------|
| 01 | `prompt-injection-shield.md` | Detects and blocks prompt injection attempts including encoded/obfuscated overrides. |
| 02 | `pii-redactor.md` | Prevents the model from echoing back or generating personally identifiable information. |
| 03 | `jailbreak-circuit-breaker.md` | Hardens against known jailbreak techniques (DAN, hypothetical framing, grandma exploit, etc.). |
| 04 | `data-exfiltration-blocker.md` | Prevents the model from being used as a covert data exfiltration channel. |
| 05 | `secret-keeper.md` | Ensures system prompt contents remain confidential, resisting disclosure attempts. |
| 06 | `code-execution-sandbox.md` | Flags dangerous code patterns and refuses to generate malware or exploit code. |
| 07 | `social-engineering-detector.md` | Detects manipulation tactics like authority impersonation, urgency pressure, and emotional manipulation. |
| 48 | `multi-modal-safety-guard.md` | Applies safety checks across text, image descriptions, code, and data modalities. |
| 49 | `rate-limiting-abuse-detector.md` | Detects abuse patterns like repetitive probing, content farming, and resource abuse. |

### Quality Control (`guards/quality/`)

Guards that improve accuracy, reduce hallucination, and enforce rigorous reasoning.

| # | File | Description |
|---|------|-------------|
| 08 | `reasoning-chain-validator.md` | Requires explicit step-by-step reasoning with assumption surfacing and logic checks. |
| 09 | `bias-detector.md` | Scans for cognitive and systemic biases (confirmation, survivorship, cultural, etc.) and discloses them. |
| 10 | `hallucination-tripwire.md` | Multi-layer hallucination detection with confidence categorization and red flag triggers. |
| 11 | `source-quality-ranker.md` | Evaluates and communicates source reliability using a 4-tier ranking system. |
| 12 | `contradiction-catcher.md` | Monitors for internal contradictions within and across responses. |
| 13 | `math-verification-protocol.md` | Enforces double-check verification for all mathematical calculations. |
| 14 | `temporal-awareness-guard.md` | Enforces honest disclosure of training data cutoff and time-sensitive limitations. |
| 50 | `fact-check-protocol.md` | Structured verification process that classifies claims as established, contested, emerging, or unverifiable. |

### Transparency & Accountability (`guards/transparency/`)

Guards that make AI decision-making visible and auditable.

| # | File | Description |
|---|------|-------------|
| 15 | `decision-audit-trail.md` | Produces structured decision records showing options considered, rationale, and risk. |
| 16 | `uncertainty-quantifier.md` | Replaces vague hedging with calibrated probability ranges and explicit uncertainty scales. |
| 17 | `capability-boundary-disclosure.md` | Proactively discloses AI limitations at the point of relevance. |
| 18 | `influence-disclosure.md` | Detects and discloses persuasion techniques and framing effects in user input. |
| 19 | `confidence-calibration.md` | Produces well-calibrated confidence scores with domain and evidence adjustments. |

### Domain-Specific (`guards/domain/`)

Guards tailored to high-stakes professional domains.

| # | File | Description |
|---|------|-------------|
| 20 | `medical-disclaimer-guard.md` | Enforces medical disclaimers, prevents diagnosis, and triggers crisis detection for emergencies. |
| 21 | `legal-disclaimer-guard.md` | Enforces legal disclaimers with jurisdictional awareness. |
| 22 | `financial-disclaimer-guard.md` | Enforces financial disclaimers and prevents specific investment recommendations. |
| 23 | `educational-scaffolding-guard.md` | Prioritizes teaching over answer-giving in learning contexts (Socratic method). |
| 24 | `cybersecurity-ethics-guard.md` | Balances security education with responsible disclosure principles. |
| 25 | `child-safety-guard.md` | Absolute protection guard for content involving minors. |
| 51 | `research-integrity-guard.md` | Enforces academic research integrity (no fabrication, proper attribution, methodology awareness). |
| 52 | `environmental-impact-awareness.md` | Surfaces environmental implications of technology and design recommendations. |
| 58 | `api-security-checklist.md` | Automated security checklist for API code generation and review. |
| 59 | `database-safety-guard.md` | Warns before destructive DB operations and enforces query safety best practices. |

### Behavioral Controls (`guards/behavioral/`)

Guards that shape how the AI conducts itself in conversation.

| # | File | Description |
|---|------|-------------|
| 26 | `scope-limiter.md` | Limits responses to the user's actual question, preventing unsolicited scope creep. |
| 27 | `task-focus-enforcer.md` | Maintains focus on the user's stated task, detects drift, and manages multi-task tracking. |
| 28 | `persona-integrity-lock.md` | Maintains consistent identity and prevents persona hijacking. |
| 29 | `refusal-grace-protocol.md` | Ensures refusals are graceful, explanatory, and always offer alternatives. |
| 30 | `sycophancy-blocker.md` | Prevents the AI from agreeing just to be agreeable — prioritizes accuracy over approval. |
| 31 | `emotional-regulation-guard.md` | Handles emotionally charged interactions with appropriate empathy and crisis resource provision. |
| 32 | `multi-turn-consistency.md` | Maintains consistency across multi-turn conversations and prevents silent contradictions. |
| 53 | `intellectual-humility-protocol.md` | Enforces honest self-assessment of knowledge depth and comfortable "I don't know" responses. |
| 60 | `cultural-sensitivity-guard.md` | Ensures cultural awareness in responses (naming, dates, customs, communication norms). |

### Operational (`guards/operational/`)

Guards that optimize efficiency, cost, and error handling.

| # | File | Description |
|---|------|-------------|
| 33 | `token-efficiency-optimizer.md` | Minimizes token usage by eliminating filler and structuring for scanning. |
| 34 | `context-window-manager.md` | Manages long conversations with checkpoints, summaries, and task decomposition. |
| 35 | `error-recovery-protocol.md` | Structured error handling with clear communication, correction protocols, and cascading checks. |
| 36 | `output-format-negotiator.md` | Matches output format to user needs with auto-detection and explicit negotiation. |
| 37 | `api-cost-guard.md` | Minimizes unnecessary API token consumption with batch awareness and structured output preferences. |
| 38 | `language-detection-responder.md` | Detects user language and responds accordingly while maintaining guard protocols across languages. |
| 55 | `graceful-degradation.md` | Degrades gracefully through 5 tiers when full responses aren't possible. |

### User Protection (`guards/user-protection/`)

Guards that protect users from harmful content, dark patterns, and privacy violations.

| # | File | Description |
|---|------|-------------|
| 39 | `consent-checkpoint.md` | Checks with the user before generating potentially unwanted or high-impact content. |
| 40 | `accessibility-advocate.md` | Embeds accessibility (a11y) best practices into all generated content and code. |
| 41 | `misinformation-firewall.md` | Prevents creation or amplification of misinformation and handles conspiracy theories constructively. |
| 42 | `privacy-by-design.md` | Embeds privacy principles (GDPR/ISO 27701) into code and architecture recommendations. |
| 43 | `content-warning-system.md` | Applies content warnings before potentially distressing material. |
| 56 | `dark-pattern-detector.md` | Detects and refuses dark pattern UI/UX implementations, suggesting ethical alternatives. |
| 57 | `digital-wellbeing-guard.md` | Optimizes engagement features for user wellbeing over addictive metrics. |

### Output Formatting (`guards/output/`)

Guards that enforce structured, consistent, and useful output formats.

| # | File | Description |
|---|------|-------------|
| 44 | `structured-output-enforcer.md` | Enforces strict JSON, CSV, and Markdown formatting for machine-consumable output. |
| 45 | `code-review-checklist.md` | Automatic security and quality checklist applied to all generated/reviewed code. |
| 46 | `citation-formatter.md` | Consistent citation formatting with honesty categories (verified, inferred, user-provided). |
| 47 | `summary-protocol.md` | Structured summarization with compression rules and multiple depth levels. |
| 54 | `diff-output-protocol.md` | Shows changes in diff format for clarity when modifying existing content. |

---

## How to Use

### Option 1: Custom Instructions (ChatGPT, Claude, etc.)
1. Open your AI's settings or custom instructions panel.
2. Copy the content of any guard file.
3. Paste it into the system prompt or custom instructions field.
4. Start chatting — the guard is now active.

### Option 2: API System Message
```python
system_message = open("guards/safety/01-prompt-injection-shield.md").read()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Your question here"}
    ]
)
```

### Option 3: Combine Multiple Guards
Stack guards for layered protection. Recommended starter pack:
```
# Core safety
guards/safety/01-prompt-injection-shield.md
guards/safety/05-secret-keeper.md

# Quality
guards/quality/10-hallucination-tripwire.md
guards/quality/12-contradiction-catcher.md

# Transparency
guards/transparency/16-uncertainty-quantifier.md
guards/transparency/19-confidence-calibration.md
```

### Token Budget
Each guard file includes an estimated token count in its header. Most guards use 200-350 tokens, making it practical to combine 3-5 guards within typical system prompt limits.

---

## Tools (`tools/`)

### Guard Combiner CLI

Combines multiple guard files into a single system prompt with token counting and budget warnings.

```bash
# List all available guards with token counts
python tools/combine.py --list-guards

# List available profiles
python tools/combine.py --list-profiles

# Combine guards from a profile
python tools/combine.py --profile developer

# Combine specific guards with a token budget
python tools/combine.py --guards safety/01 quality/10 transparency/16 --budget 2000

# Save combined prompt to a file
python tools/combine.py --profile maximum-security --output system_prompt.txt

# Budget presets: small (1K), medium (2K), standard (4K), large (8K), xlarge (16K)
python tools/combine.py --profile researcher --budget standard
```

### Prompt Linter

Analyzes any system prompt for common weaknesses and produces a scored security report. Works on any prompt — not just PromptProof guards.

```bash
# Lint a prompt file
python tools/lint_prompt.py my_system_prompt.txt

# Lint from stdin
echo "You are a helpful assistant." | python tools/lint_prompt.py --stdin

# Output as JSON (for CI/CD pipelines)
python tools/lint_prompt.py my_prompt.txt --json > report.json
```

The linter checks for 14 categories including: injection protection, hallucination controls, PII handling, secret protection, crisis handling, domain disclaimers, bias awareness, and more. Each check is rated CRITICAL, HIGH, MEDIUM, LOW, or INFO, and the overall score (0-100) grades your prompt as STRONG, MODERATE, WEAK, or VULNERABLE.

### Benchmark Runner

Measures guard effectiveness by running adversarial test prompts against an LLM with and without guards, comparing pass rates.

```bash
# Dry run — list all tests without API calls
python tools/benchmark.py --dry-run --guard guards/safety/01-prompt-injection-shield.md

# Run against OpenAI
python tools/benchmark.py --provider openai --model gpt-4 --guard guards/safety/01-prompt-injection-shield.md

# Run against Anthropic
python tools/benchmark.py --provider anthropic --model claude-sonnet-4-20250514 --profile developer

# Run against local Ollama
python tools/benchmark.py --provider ollama --model llama3 --profile maximum-security

# Save results as JSON
python tools/benchmark.py --provider openai --model gpt-4 --profile developer --json -o results.json
```

---

## Adversarial Test Suite (`tests/`)

44 adversarial test prompts across 8 categories, designed to probe LLM vulnerabilities:

| Category | Tests | What it probes |
|----------|-------|----------------|
| `injection` | 8 | Prompt injection and instruction override attempts |
| `jailbreak` | 6 | DAN, hypothetical framing, grandma exploit, developer mode |
| `pii` | 5 | PII echoing, generation, and extraction |
| `hallucination` | 6 | Fabricated citations, future events, fake entities |
| `social_engineering` | 5 | Authority impersonation, urgency pressure, emotional manipulation |
| `extraction` | 7 | System prompt disclosure and extraction techniques |
| `domain` | 6 | Medical, legal, financial safety and crisis handling |
| `code_safety` | 6 | Dangerous code generation, injection vectors, malware |

```bash
# List all test suites
python tests/run_tests.py --list

# Run all tests with HTML report
python tests/run_tests.py --provider openai --model gpt-4 --profile developer --report

# Run a specific test category
python tests/run_tests.py --provider openai --model gpt-4 --profile maximum-security --category injection
```

The HTML report shows before/after comparisons with per-category breakdowns and details on failed tests.

---

## Preset Profiles (`profiles/`)

Pre-built guard combinations for common use cases. Each profile is a curated set of guards that work well together.

| Profile | Guards | Focus |
|---------|--------|-------|
| `developer` | 8 | Code safety, quality, reasoning, token efficiency |
| `researcher` | 10 | Accuracy, citations, bias detection, intellectual rigor |
| `educator` | 7 | Teaching-first approach, accessibility, cultural sensitivity |
| `customer-support` | 9 | PII protection, emotional handling, multi-language, consistency |
| `children` | 9 | Maximum safety, age-appropriate content, education |
| `healthcare` | 10 | Medical disclaimers, privacy, crisis handling, uncertainty |
| `content-creator` | 8 | Accuracy, misinformation prevention, ethical content |
| `maximum-security` | 15 | All safety guards active — for regulated environments |

```bash
# Use a profile with the combiner
python tools/combine.py --profile developer --output my_prompt.txt

# Benchmark a profile
python tools/benchmark.py --provider openai --model gpt-4 --profile maximum-security
```

---

## Integration Templates (`integrations/`)

Ready-to-use code for wiring PromptProof guards into popular LLM frameworks. Each template includes guard loading, profile support, streaming, and conversation history.

| File | Provider | Dependencies |
|------|----------|-------------|
| `openai_integration.py` | OpenAI (GPT-4, GPT-4o, etc.) | `pip install openai` |
| `anthropic_integration.py` | Anthropic (Claude) | `pip install anthropic` |
| `ollama_integration.py` | Ollama (local LLMs) | None (uses urllib) |
| `langchain_integration.py` | LangChain (any provider) | `pip install langchain langchain-openai` |
| `llamaindex_integration.py` | LlamaIndex (RAG pipelines) | `pip install llama-index` |

Each integration supports:
- Loading single guards or full profiles
- Streaming and non-streaming responses
- Conversation history management
- Interactive chat loop for testing

```bash
# Run the OpenAI integration demo
export OPENAI_API_KEY=sk-...
python integrations/openai_integration.py

# Run with local Ollama (no API key needed)
python integrations/ollama_integration.py
```

---

## Benchmarks (`benchmarks/`)

Reference scores and generated reports live here.

- `reference-scores.json` — Estimated effectiveness scores for each profile and individual guards across test categories. Use as a baseline to compare your own benchmark results.
- `report.html` — Generated by the test runner with `--report` flag. Visual before/after comparison.

---

## Project Structure

```
PromptProof/
├── guards/                    # 60 guardrail prompt files
│   ├── safety/                # Injection, PII, jailbreak protection
│   ├── quality/               # Hallucination, bias, reasoning checks
│   ├── transparency/          # Audit trails, uncertainty, disclosure
│   ├── domain/                # Medical, legal, financial, education
│   ├── behavioral/            # Scope, consistency, refusal, empathy
│   ├── operational/           # Efficiency, error handling, formatting
│   ├── user-protection/       # Privacy, accessibility, content warnings
│   └── output/                # Structured output, citations, diffs
├── profiles/                  # Pre-built guard combinations
├── tools/                     # CLI utilities
│   ├── combine.py             # Guard combiner with token budgets
│   ├── lint_prompt.py         # System prompt security linter
│   └── benchmark.py           # Guard effectiveness benchmarker
├── tests/
│   ├── adversarial/           # 44 adversarial test prompts (JSON)
│   └── run_tests.py           # Test runner with HTML reporting
├── integrations/              # Drop-in code for OpenAI, Anthropic, Ollama, LangChain, LlamaIndex
├── benchmarks/                # Reference scores and generated reports
├── SpeculationSpeedBump.txt   # Original guard
├── Ethical-Guard              # Original guard
├── Notify_of_AI_usage         # Original guard
├── Resource_Maximizer         # Original prompt
├── about.md                   # Project description
├── LICENSE                    # GPL v3
└── README.md                  # This file
```

---

## Contributing

1. Fork the repo
2. Create a new guard file following the existing format (header with name, estimated tokens, category, then the directive)
3. Place it in the appropriate `guards/<category>/` directory
4. Run the linter on your guard: `python tools/lint_prompt.py your_guard.md`
5. Submit a pull request with a clear description of what the guard does and why it's needed

To add new adversarial tests, create a JSON file in `tests/adversarial/` following the existing format.

---

## License

GPL v3 — see [LICENSE](LICENSE) for details.
