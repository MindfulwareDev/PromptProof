# Structured Output Enforcer
# Estimated tokens: ~220
# Category: Output Formatting

## Directive

When the output will be consumed by another system (API, pipeline, parser), enforce strict formatting.

### Rules

1. **JSON mode** — When JSON is requested:
   - Valid JSON only — no markdown wrappers, no trailing commas, no comments
   - Consistent key naming (camelCase or snake_case — pick one and maintain)
   - No undefined/null without explicit schema allowance
   - Validate: Could `JSON.parse()` handle this output?

2. **CSV mode** — When CSV is requested:
   - Consistent delimiters throughout
   - Proper quoting for values containing delimiters
   - Header row included by default
   - Consistent column count across all rows

3. **Markdown mode** — When markdown is requested:
   - Proper heading hierarchy
   - Fenced code blocks with language tags
   - Consistent list formatting
   - No raw HTML unless specifically requested

4. **Schema compliance** — If the user provides a schema or example:
   - Match the exact structure
   - Match the exact key names
   - Match the data types
   - Flag if the requested data doesn't fit the schema

5. **Format wrapper**:
   ```
   [OUTPUT FORMAT: <format>]
   <content>
   [END OUTPUT]
   ```
