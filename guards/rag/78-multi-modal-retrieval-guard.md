# Multi-Modal Retrieval Guard
# Estimated tokens: ~290
# Category: RAG (Retrieval-Augmented Generation)
# Contributor: Daniel Joye

## Directive

Apply appropriate handling when the RAG corpus includes non-text content such as images, tables, charts, diagrams, or embedded media that may be retrieved alongside text.

### Rules

1. **Modality awareness** — Identify the content type of each retrieved chunk:
   ```
   [CONTENT TYPES] Retrieved: 3 text passages, 1 table, 1 image description
   ```

2. **Table handling** — When retrieved content includes tabular data:
   - Preserve table structure in the response
   - Do not paraphrase tables into prose unless asked
   - Flag if the table appears truncated or split across chunks
   ```
   [TABLE DATA] Source: <filename>, Table: <title/description>
   ```

3. **Image/diagram references** — When chunks reference visual content:
   ```
   [VISUAL REFERENCE] The source document includes a diagram/image at this point
   (<description if available>). The visual content cannot be displayed here.
   Refer to <filename>, <page/section> for the original.
   ```

4. **OCR content caution** — If retrieved text appears to be OCR output:
   ```
   [OCR SOURCE] This content may be from scanned/OCR'd documents.
   Formatting errors or misread characters are possible.
   ```

5. **Structured data** — When retrieved chunks contain JSON, XML, or code:
   - Present in appropriate code blocks
   - Don't attempt to "translate" structured data into prose
   - Flag if the data appears to be a partial/truncated extract
