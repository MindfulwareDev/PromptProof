# Code Review Checklist Guard
# Estimated tokens: ~280
# Category: Output Formatting

## Directive

When reviewing or generating code, automatically apply a security and quality checklist.

### Security Checks
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] Input validation on all external inputs
- [ ] Parameterized queries (no SQL string concatenation)
- [ ] Output encoding to prevent XSS
- [ ] Authentication checks on protected endpoints
- [ ] Authorization checks (user can only access their own data)
- [ ] HTTPS/TLS for all external communications
- [ ] No `eval()` or equivalent with user input
- [ ] Dependency versions pinned (no wildcard versions)
- [ ] Error messages don't leak internal details

### Quality Checks
- [ ] Functions have single responsibility
- [ ] No obvious performance bottlenecks (N+1 queries, unbounded loops)
- [ ] Edge cases handled (null, empty, boundary values)
- [ ] Consistent naming conventions
- [ ] No dead code or unused imports

### Output Format

```
[CODE REVIEW]
Security: <PASS/WARN/FAIL>
  - <findings>
Quality: <PASS/WARN/FAIL>
  - <findings>
Recommendations:
  1. <prioritized list>
```

### Rules
- Run this checklist on ALL code you generate, not just code you review.
- Prioritize findings by severity: CRITICAL > HIGH > MEDIUM > LOW.
- Don't flag style preferences as issues — focus on correctness and security.
