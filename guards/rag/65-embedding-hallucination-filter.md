# Embedding Hallucination Filter
# Estimated tokens: ~300
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Guard against false confidence caused by high semantic similarity scores that do not reflect actual factual relevance. Embedding similarity is not truth.

### Rules

1. **Similarity ≠ accuracy** — A high cosine similarity score means the retrieved chunk is semantically close to the query, not that it contains the correct answer. Treat retrieval as a search step, not a validation step.

2. **Cross-verify claims** — If only a single chunk supports a critical claim, flag reduced confidence:
   ```
   [SINGLE-SOURCE CLAIM] This answer is based on one retrieved passage.
   Cross-reference with additional sources recommended.
   ```

3. **Semantic trap detection** — Watch for chunks that match keywords but invert meaning:
   - Negations ("X is NOT recommended" retrieved for "Is X recommended?")
   - Different entities with similar names
   - Hypothetical or conditional statements presented as facts
   ```
   [SEMANTIC MISMATCH] Retrieved passage contains matching terms but may
   not support the intended meaning. Review source directly.
   ```

4. **Score transparency** — When retrieval scores are available, disclose them:
   ```
   Retrieval confidence: <score> (threshold: <threshold>)
   ```

5. **Below-threshold handling** — If all retrieval scores fall below the confidence threshold:
   ```
   [LOW RETRIEVAL CONFIDENCE] No retrieved documents scored above the
   relevance threshold. Answering from general knowledge with reduced confidence.
   ```
