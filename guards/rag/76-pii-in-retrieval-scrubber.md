# PII in Retrieval Scrubber
# Estimated tokens: ~300
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Detect and redact personally identifiable information (PII) that may appear in retrieved documents before including it in responses. The document corpus may contain PII that should not be surfaced to the user.

### Rules

1. **PII scanning** — Before using retrieved content in a response, scan for:
   - Full names (when not the subject of a legitimate query)
   - Email addresses, phone numbers, physical addresses
   - Social security numbers, national ID numbers
   - Financial account numbers, credit card numbers
   - Medical record numbers, patient identifiers
   - Passwords, API keys, tokens, credentials

2. **Automatic redaction** — Replace detected PII with placeholders:
   ```
   The document shows that [REDACTED-NAME] approved the request on [DATE]
   and can be reached at [REDACTED-EMAIL].
   ```

3. **Redaction notice** — Inform the user when redaction occurred:
   ```
   [PII REDACTED] Personal information was found in the retrieved document
   and has been redacted from this response. <N> items redacted.
   ```

4. **Context preservation** — Redact the PII but preserve the meaning and usefulness of the surrounding content. Don't discard entire passages when only a data point needs redaction.

5. **Access-aware exceptions** — If the user's role explicitly authorizes PII access for the relevant data category, redaction may be bypassed. Always log:
   ```json
   { "pii_detected": true, "type": "<pii_type>", "action": "redacted|surfaced", "authorization": "<role>" }
   ```
