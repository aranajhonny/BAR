# BAR — Book Agentic RAG

**Current status: functional.** An agentic RAG backend that answers questions about your technical PDF library. LangGraph orchestrates: a Router node decides which book to search, a Retrieval node searches Qdrant with small-to-big chunking, and a Generation node answers only from that context. No web search, no hallucination.

## Stack

- **LangGraph** — orchestration with `StateGraph`
- **LangChain + OpenAI-compatible** — embeddings and generation (via opencode.ai)
- **Qdrant** — vector store (local, Docker)
- **FastAPI** — API
- **pypdf** — text extraction
- **fastembed** — local embeddings (BGE Small)

## Quick start

```bash
# 1. Environment
python3 -m venv .venv && source .venv/bin/activate && pip install -e .

# 2. Variables
cp .env.example .env   # add your OPENCODE_API_KEY

# 3. Qdrant
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

# 4. Index a PDF
python scripts/ingest.py data/your-book.pdf

# 5. Start server
uvicorn app.main:app --reload

# 6. Ask
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "what is X", "thread_id": "test"}'
```

## UI

A minimal chat interface is available at `http://localhost:9999`.

```bash
python3 -m http.server 9999 --directory app/static
```

## License

MIT
