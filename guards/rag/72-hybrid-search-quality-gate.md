# Hybrid Search Quality Gate
# Estimated tokens: ~280
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

When using hybrid retrieval (combining semantic/vector search with keyword/BM25 search), validate that results from both methods are reconciled properly before generating a response.

### Rules

1. **Dual-method awareness** — Acknowledge when results come from different retrieval methods:
   ```
   [RETRIEVAL METHOD] Results from: semantic search (<N> chunks), keyword search (<M> chunks).
   ```

2. **Cross-method validation** — Chunks appearing in both semantic and keyword results receive a confidence boost. Chunks from only one method should be treated with moderate confidence.

3. **Keyword-only results** — When keyword search returns results that semantic search missed:
   - Likely contains exact terminology or identifiers the user specified
   - May be highly relevant despite lower semantic similarity
   - Give preference when the user's query contains specific terms, codes, or names

4. **Semantic-only results** — When semantic search returns results that keyword search missed:
   - May capture intent even if the user used different terminology
   - Verify that the conceptual match is genuinely relevant, not a false semantic neighbor

5. **Retrieval method failure** — If one method returns zero results:
   ```
   [RETRIEVAL NOTE] <method> search returned no results.
   Answer is based solely on <other_method> search results.
   ```

6. **Deduplication** — Merge near-identical chunks from both methods before response generation to avoid repetitive answers.
