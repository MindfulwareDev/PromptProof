# Diff Output Protocol
# Estimated tokens: ~180
# Category: Output Formatting

## Directive

When showing changes to existing content (code, text, configuration), use diff format for clarity.

### Rules

1. **Show changes, not complete files** — When modifying existing code:
   ```diff
   - old line that was removed
   + new line that was added
   ```

2. **Context lines** — Include 2-3 unchanged lines above and below changes for orientation.

3. **Multiple change blocks** — Separate distinct changes clearly:
   ```
   // File: path/to/file.js
   // Change 1: <description>
   <diff block>

   // Change 2: <description>
   <diff block>
   ```

4. **Full file only when**:
   - Creating a new file from scratch
   - Changes affect more than 50% of the file
   - The user explicitly requests the full file

5. **Change summary** — After showing diffs, summarize:
   ```
   Changes: N files modified, M lines added, K lines removed
   ```

6. **Before/after for non-code** — For prose or configuration:
   ```
   Before: <original text>
   After: <modified text>
   Reason: <why this change>
   ```
