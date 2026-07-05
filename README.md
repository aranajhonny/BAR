# Book Agentic RAG Backend

A lightweight, production-ready agentic RAG backend engineered specifically for navigating and studying dense, comprehensive technical textbooks and PDF material. Built completely by hand without high-level magic frameworks, using **Python, FastAPI, LangGraph, and Qdrant**.

Unlike standard RAG implementations optimized for short research papers, this architecture handles long-form books by leveraging hierarchical context parenting and an explicit state-machine graph loop that enforces deterministic tool selection and execution steps.

## 🚀 Technical Stack

* **Orchestration & State Machine:** `langgraph` (Explicit Node & Edge execution topology)
* **LLM & Tool Binding Abstractions:** `langchain-core` / `langchain-openai`
* **Web Ingestion & Fallback Research:** `Exa API` / `Tavily` (Filtered exclusively for engineering and academic sources)
* **Vector Infrastructure:** `Qdrant` (Running via local Docker container)
* **API Framework:** `FastAPI` (Asynchronous endpoints supporting live execution streaming)

---

## 📐 Architecture Flow

The system operates as a State Machine Graph (`StateGraph`), evaluating queries against a strict execution topology:

1.  **User Input:** Accepts queries alongside a unique `thread_id` to persist chat history across interactions.
2.  **Agent/Router Node:** Evaluates the user query against available tools using structured JSON Tool Calling schema.
3.  **Execution Nodes (Parallel):**
    * **Local Retrieval (Qdrant):** Performs cosine similarity lookups over dense book vectors. Returns high-density parent chunks bundled with strict metadata tracking (Title, Chapter, Page).
    * **External Search (Exa):** Triggers if local book knowledge is insufficient, falling back to highly curated academic web schemas.
4.  **Consolidation & Generation Node:** Merges the `context_pool` with active thread messages, feeding an advanced Academic Synthesizer prompt to generate the streaming output.

---

## 🗂️ Project Scaffolding

```text
├── app/
│   ├── api/             # FastAPI routing layers and endpoints
│   ├── core/            # Core Agent Engine (graph.py, state.py, prompts.py)
│   ├── database/        # Connection setups and structural schemas
│   ├── tools/           # Custom tool handlers (vector_db.py, web_search.py)
│   └── config.py        # Environment variables type validation
├── scripts/
│   └── ingest.py        # High-density PDF chunking and indexing script
├── .env                 # Local secrets and API credentials storage
├── plan.md              # Technical execution step-by-step checklist
└── pyproject.toml       # Environment lock and dependency manifest
