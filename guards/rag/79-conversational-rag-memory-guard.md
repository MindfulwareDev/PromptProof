# Conversational RAG Memory Guard
# Estimated tokens: ~300
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

In multi-turn RAG conversations, manage the interplay between conversation history, previously retrieved context, and new retrievals. Prevent context contamination and memory confusion.

### Rules

1. **Fresh retrieval per turn** — Each new question should trigger a fresh retrieval pass. Do not reuse stale retrieved context from earlier turns unless the question explicitly references it.

2. **Context provenance tracking** — Distinguish between:
   - **Retrieved now** — Freshly retrieved for the current query
   - **Retrieved earlier** — From a previous turn in this conversation
   - **User-stated** — Information the user provided directly
   - **Inferred** — Conclusions drawn from combining sources

3. **Carry-forward disclosure** — If reusing context from a previous turn:
   ```
   [PRIOR CONTEXT] This answer incorporates information retrieved in
   an earlier turn of this conversation (Turn <N>).
   ```

4. **Contradictions across turns** — If new retrieval contradicts information from earlier turns:
   ```
   [UPDATED INFORMATION] New retrieval results differ from information
   provided earlier in this conversation.
   Previous: <old_info>
   Current: <new_info>
   ```

5. **Memory scope** — Do not let the accumulated conversation context cause the model to drift from the retrieved evidence. Each answer should still be grounded in current retrieval results.

6. **Topic shift detection** — When the user changes topic, clear implicit context assumptions from previous turns:
   ```
   [TOPIC SHIFT DETECTED] Retrieving fresh context for new topic.
   ```
