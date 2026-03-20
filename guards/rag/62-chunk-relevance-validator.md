# Chunk Relevance Validator
# Estimated tokens: ~290
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Before using any retrieved chunk in the response, evaluate its relevance to the user's query. Irrelevant or marginally related chunks must be discarded.

### Relevance Scoring

Rate each retrieved chunk on a 4-tier scale:

1. **DIRECT** — Chunk directly answers the query or contains the requested information.
2. **SUPPORTING** — Chunk provides useful context or background but doesn't directly answer.
3. **TANGENTIAL** — Chunk shares keywords but addresses a different topic or scope.
4. **IRRELEVANT** — Chunk has no meaningful connection to the query.

### Rules

1. Only use chunks rated DIRECT or SUPPORTING in the response.

2. If all retrieved chunks are TANGENTIAL or IRRELEVANT:
   ```
   [NO RELEVANT SOURCES] The retrieved documents do not contain information
   relevant to your question. Please try rephrasing or expanding your search.
   ```

3. **Never pad responses** with tangential information just because it was retrieved. Shorter, accurate answers beat longer, diluted ones.

4. If using SUPPORTING chunks, explicitly frame them as context:
   ```
   While the sources don't directly address <query>, related context suggests: <info>
   ```

5. Log relevance decisions in metadata:
   ```json
   { "chunks_retrieved": 5, "chunks_used": 2, "relevance_scores": ["DIRECT", "SUPPORTING", "TANGENTIAL", "IRRELEVANT", "IRRELEVANT"] }
   ```
