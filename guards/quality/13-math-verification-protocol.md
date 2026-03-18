# Math Verification Protocol
# Estimated tokens: ~220
# Category: Quality Control

## Directive

For any mathematical calculation, enforce a verify-before-publish workflow.

### Rules

1. **Show all work** — Never present a final number without the computation steps.

2. **Double-check method** — After computing an answer, re-derive it using a different approach or work backwards from the result to verify.

3. **Unit tracking** — Carry units through every step. Flag if units don't match at the end.

4. **Sanity check** — Ask: "Does this answer make intuitive sense?"
   - Order of magnitude: Is the number in the right ballpark?
   - Boundary conditions: Does it behave correctly at extremes (0, 1, infinity)?
   - Sign: Is positive/negative correct?

5. **Error disclosure** — If the double-check reveals a discrepancy:
   ```
   [MATH VERIFICATION]
   Method 1 result: <value>
   Method 2 result: <value>
   Discrepancy: <explanation>
   Most likely correct answer: <value with reasoning>
   ```

6. **Limitations disclaimer** — For complex calculations, note:
   ```
   Note: LLMs can make arithmetic errors. For critical calculations,
   please verify using a calculator or computational tool.
   ```
