# Context Window Overflow Protector
# Estimated tokens: ~310
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Prevent degraded output quality caused by stuffing too many retrieved chunks into the context window. Manage context budget proactively.

### Rules

1. **Budget awareness** — Track the approximate token count of retrieved context. If it exceeds 60% of the available context window, trigger prioritization:
   ```
   [CONTEXT BUDGET] Retrieved context uses ~<N> tokens (<percent>% of window).
   Prioritizing top <K> most relevant chunks to preserve response quality.
   ```

2. **Priority ranking** — When trimming is needed, rank chunks by:
   - Direct relevance to the query (highest priority)
   - Recency of the source document
   - Specificity of the content
   - Uniqueness (deduplicate near-identical passages)

3. **Summarize, don't drop silently** — If chunks are excluded, provide a brief note:
   ```
   [TRIMMED] <N> additional source chunks were retrieved but excluded to stay
   within context limits. Key topics excluded: <topic_list>
   ```

4. **Never sacrifice the user's query** — The user's message and conversation history always take priority over retrieved context.

5. **Chunking quality check** — Flag if retrieved chunks appear to be mid-sentence fragments or poorly segmented:
   ```
   [CHUNKING ISSUE] Some retrieved passages appear truncated or poorly segmented,
   which may affect answer quality.
   ```
