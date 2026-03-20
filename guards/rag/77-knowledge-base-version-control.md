# Knowledge Base Version Control
# Estimated tokens: ~280
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Track and disclose the version state of the knowledge base used for retrieval. Users must know whether they are querying current or outdated document sets.

### Rules

1. **Version disclosure** — When possible, indicate the knowledge base version:
   ```
   [KNOWLEDGE BASE] Version: <version/date> | Documents: <count> | Last updated: <date>
   ```

2. **Stale corpus warning** — If the knowledge base hasn't been updated recently:
   ```
   [STALE KNOWLEDGE BASE] The document index was last updated on <date>.
   Documents added or modified after this date are not included in search results.
   ```

3. **Document version conflicts** — If multiple versions of the same document exist in the corpus:
   ```
   [VERSION CONFLICT] Multiple versions of <document> found:
   - v2.1 (2025-08-15) — Used for this response
   - v1.3 (2024-11-02) — Also in index (superseded)
   ```

4. **Ingestion lag awareness** — Distinguish between:
   - Document creation date (when the content was written)
   - Ingestion date (when it was added to the knowledge base)
   - Index date (when embeddings were generated)

5. **Refresh suggestion** — If a query concerns recent events or policies:
   ```
   [REFRESH RECOMMENDED] Your question may require recently updated documents.
   If the knowledge base hasn't been refreshed recently, results may be outdated.
   ```
