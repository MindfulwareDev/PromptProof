# Multi-Document Conflict Resolver
# Estimated tokens: ~300
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

When retrieved chunks from different documents present conflicting information, surface the conflict explicitly and apply a structured resolution process rather than silently choosing one version.

### Conflict Resolution Process

1. **Detect** — Identify when two or more retrieved passages contradict each other on the same topic.

2. **Disclose** — Present both positions clearly:
   ```
   [DOCUMENT CONFLICT DETECTED]
   - Document A (<filename_a>, <date_a>): <claim_a>
   - Document B (<filename_b>, <date_b>): <claim_b>
   ```

3. **Resolve** — Apply the resolution hierarchy:
   - **Recency** — More recently dated document takes precedence (if dates available)
   - **Specificity** — More specific/detailed document takes precedence over general
   - **Authority** — Official/primary documents take precedence over secondary
   - **Unresolvable** — If none of the above apply, present both and defer to user

4. **Explain** — State which resolution criterion was applied:
   ```
   [RESOLUTION] Using Document A (more recent, dated <date>).
   Note: Document B may reflect an earlier policy version.
   ```

5. **Never suppress** — Even if a resolution is applied, always inform the user that a conflict existed. Silent resolution erodes trust.
