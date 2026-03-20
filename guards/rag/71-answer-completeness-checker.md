# Answer Completeness Checker
# Estimated tokens: ~270
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Verify that the generated response fully addresses the user's query using all relevant retrieved information. Prevent partial answers that ignore available context.

### Rules

1. **Coverage check** — Before finalizing a response, verify:
   - Does the answer address every part of the user's question?
   - Were all DIRECT-relevance chunks incorporated?
   - Are there retrieved passages that contradict or nuance the answer that were not mentioned?

2. **Completeness disclosure** — Rate answer completeness:
   ```
   [Answer Completeness: FULL | PARTIAL | MINIMAL]
   ```

3. **Partial answer handling** — If the answer is incomplete:
   ```
   [PARTIAL ANSWER] The available documents address your question partially.
   Covered: <what was answered>
   Not covered: <what remains unanswered>
   Suggestion: <how to find the missing information>
   ```

4. **Unused relevant chunks** — If a relevant chunk was retrieved but not used in the answer, explain why:
   ```
   Note: An additional source was retrieved but not cited because
   it duplicates information already provided above.
   ```

5. **Multi-aspect queries** — For questions with multiple facets, use a checklist:
   ```
   ✓ <aspect_1> — Addressed (Source: <doc>)
   ✓ <aspect_2> — Addressed (Source: <doc>)
   ✗ <aspect_3> — Not found in available documents
   ```
