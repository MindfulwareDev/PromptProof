# Contributing to PromptProof

Thanks for your interest in making LLMs safer and more accountable! Here's how to contribute.

## Ways to Contribute

### Add a New Guard
1. Fork the repo and create a branch.
2. Create a `.md` file in the appropriate `guards/<category>/` directory.
3. Follow this format:
   ```markdown
   # Guard Name – Optional Subtitle
   # Estimated tokens: ~NNN
   # Category: <category name>

   ## Directive

   <Your guard instructions here>

   ### Rules
   1. <Rule 1>
   2. <Rule 2>
   ...
   ```
4. Run the linter to check quality: `python tools/lint_prompt.py your_guard.md`
5. Submit a PR with a clear description of what the guard does and why it's needed.

### Add Adversarial Tests
1. Create a JSON file in `tests/adversarial/` following this format:
   ```json
   {
     "name": "Test Suite Name",
     "category": "category_name",
     "description": "What these tests probe",
     "prompts": [
       {
         "text": "The adversarial prompt",
         "expected_behavior": {
           "should_refuse": true,
           "should_disclaim": false,
           "should_not_leak": false,
           "should_label_uncertainty": false
         }
       }
     ]
   }
   ```
2. Test with `--dry-run` first: `python tests/run_tests.py --dry-run`

### Add Integration Templates
- Follow the pattern in `integrations/` — each template should include guard/profile loading, streaming support, and a working example.

### Improve Existing Guards
- Better wording, fewer tokens, broader coverage — all welcome.
- Run the linter before and after to verify improvements.

## Guidelines

- **Keep guards self-contained** — Each guard should work independently when pasted into a system prompt.
- **Minimize tokens** — Every token counts in a system prompt budget. Aim for under 350 tokens per guard.
- **Test your work** — Use the linter and, if possible, test against a real LLM.
- **No breaking changes** — Existing guards and profiles should continue to work.

## Code of Conduct

Be respectful, constructive, and focused on making AI safer for everyone.

## Questions?

Open an issue — happy to discuss ideas before you start coding.
