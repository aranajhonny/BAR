# BAR — Book Agentic RAG

There's a question that haunts anyone trying to study a dense technical textbook: where exactly was that idea I read three chapters ago? BAR exists because of that friction. It's an agentic RAG backend, closed over your own PDF library, built to answer that precisely — never to make something up.

This isn't a product. It's a deliberate exercise: actually learning LangChain and LangGraph by building something that uses them for real, instead of copying a tutorial. Python, FastAPI, LangGraph, and Qdrant are the playground.

## Philosophy

The agent lives inside a strict boundary: it only knows what you gave it to read. No web search, no leaking into the model's general knowledge. If the answer isn't in your books, the system admits it instead of filling the gap with a confident hallucination. That restriction isn't a limitation — it's the whole point of the design.

## The stack, and why

- **LangGraph** as the orchestration engine: an explicit `StateGraph` with nodes and edges you could sketch on a whiteboard before writing a line of code.
- **LangChain core / langchain-openai** for structured tool-calling.
- **Qdrant** as the vector memory, running locally in Docker.
- **FastAPI** as the entry point, with async streaming.

Worth saying plainly: this project uses frameworks on purpose. The goal is understanding LangGraph from the inside — its nodes, its shared state, its routing decisions — not avoiding it to prove some kind of technical purity. The craftsmanship is in the graph and retrieval design, not in rejecting the tooling.

## How the graph thinks

```
User query + thread_id
        │
        ▼
   Router Node          (structured tool-calling: which book, which chapter?)
        │
        ▼
   Retrieval Node        (cosine similarity over Qdrant, small-chunk lookup
        │                 → expanded to parent chunk)
        ▼
   Generation Node        (merges retrieved context + thread history,
                            streams the answer)
```

If retrieval finds nothing relevant, the generation node is instructed to say so plainly, not improvise.

## Project layout

```
├── app/
│   ├── api/          # FastAPI routes
│   ├── core/         # graph.py, state.py, prompts.py
│   ├── database/     # connection + schema
│   ├── tools/         # vector_db.py and other tool handlers
│   └── config.py      # env var validation
├── scripts/
│   └── ingest.py       # PDF chunking + indexing
├── tests/
│   └── test_graph_smoke.py   # end-to-end: query → retrieval → generation
├── .env
├── PLAN.md
└── pyproject.toml
```

## Getting started

### 1. Clone and set up the environment

```bash
git clone <your-repository-url>
cd book-agentic-rag

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # or uv / poetry
```

### 2. Environment variables

Create `.env` in the project root:

```
OPENAI_API_KEY=your_openai_key_here
QDRANT_URL=http://localhost:6333
```

Honest caveat: embeddings and generation currently go through the OpenAI API. "Closed" here means knowledge is bounded to your library, not that inference runs 100% on your machine. If that matters to you as a next learning step, swapping in a local embedding model plus a local LLM (Ollama, say) is a natural extension — it's in PLAN.md.

### 3. Spin up Qdrant

```bash
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

Dashboard: http://localhost:6333/dashboard

### 4. Ingest your PDFs

Drop your PDFs into the data folder, then:

```bash
python scripts/ingest.py
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

## Design decisions worth understanding

**Small-to-big chunking.** Qdrant indexes short chunks (~200 tokens) because they're better for similarity search. But a chunk that small, on its own, starves the answer of context — so retrieval expands each hit to its full parent chunk (~1200 tokens) before it reaches the prompt. Precision in the search, richness in the context.

**Bounded knowledge.** No web search tool is bound to the agent. The system prompt forces it to answer only from the retrieved `context_pool`. This is a design and prompting constraint, not a hard technical guarantee against hallucination — worth keeping in mind while learning where the real limits of this technique sit.

**Metadata slicing.** Every vector carries `book_title`, `chapter_number`, and `page`, so the Router node can constrain a search to a specific book or chapter when the query implies it.

## Status

Early stage, on purpose: retrieval and generation work end-to-end, but test coverage today is a single smoke test (see `tests/`). See PLAN.md for the rest of the learning path.

## License

MIT
