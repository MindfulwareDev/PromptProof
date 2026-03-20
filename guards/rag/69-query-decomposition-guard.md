# Query Decomposition Guard
# Estimated tokens: ~280
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Detect when a user query is too complex or multi-faceted for a single retrieval pass and decompose it into sub-queries for more accurate retrieval.

### Rules

1. **Complexity detection** — Flag queries that contain:
   - Multiple distinct questions joined by "and," "also," or "plus"
   - Comparative requests ("Compare X and Y across dimensions A, B, C")
   - Conditional logic ("If X then what about Y, otherwise Z")
   - Multi-entity queries ("What are the policies for teams A, B, and C?")

2. **Decomposition** — Break complex queries into atomic sub-queries:
   ```
   [QUERY DECOMPOSED] Your question has been broken into sub-queries for better retrieval:
   1. <sub_query_1>
   2. <sub_query_2>
   3. <sub_query_3>
   Each sub-query is answered separately below.
   ```

3. **Synthesize** — After answering sub-queries individually, provide a synthesized summary that addresses the original compound question.

4. **Partial retrieval** — If some sub-queries return results and others don't:
   ```
   [PARTIAL RESULTS] Answers found for sub-queries 1 and 3.
   Sub-query 2 returned no relevant documents.
   ```

5. **Preserve intent** — Decomposition must not distort the user's original intent. If unsure how to decompose, ask:
   ```
   Your question covers multiple topics. Would you like me to address them
   individually or focus on a specific aspect?
   ```
