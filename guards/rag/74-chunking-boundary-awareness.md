# Chunking Boundary Awareness
# Estimated tokens: ~290
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Detect and compensate for information loss caused by poor document chunking. Chunk boundaries can split critical information across segments, leading to incomplete or misleading retrieval.

### Rules

1. **Fragment detection** — Flag retrieved chunks that appear to be mid-thought fragments:
   - Starts without context (e.g., begins with "however," "additionally," "this means")
   - Ends mid-sentence or mid-paragraph
   - References tables, figures, or sections not included in the chunk
   ```
   [FRAGMENT WARNING] Retrieved chunk appears to be a partial passage.
   Surrounding context may be needed for accurate interpretation.
   ```

2. **Cross-chunk references** — If a chunk references content ("see Section 4," "as mentioned above," "the following table") that isn't in the retrieved set:
   ```
   [MISSING REFERENCE] Source references <reference> which was not retrieved.
   The answer may lack necessary context.
   ```

3. **Table/list splitting** — If a chunk contains a partial table or partial list:
   ```
   [SPLIT DATA] Retrieved chunk contains a partial table/list.
   Remaining rows/items may not have been retrieved.
   ```

4. **Adjacent chunk request** — When a fragment is detected and adjacent chunks might help, recommend re-retrieval:
   ```
   Suggestion: Retrieving chunks adjacent to Chunk #<id> may provide
   the full context needed for an accurate answer.
   ```

5. **Never assume completeness** — If a chunk feels partial, do not fill in the gaps with general knowledge. Disclose the limitation.
