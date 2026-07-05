# Book Agentic RAG Backend (100% Local RAG)

A lightweight, production-ready agentic RAG backend engineered specifically for navigating and studying dense, comprehensive technical textbooks and PDF material. Built completely by hand without black-box abstractions, using **Python, FastAPI, LangGraph, and Qdrant**.

This backend operates as a completely **closed-domain system**. It does not connect to the internet or external search engines. The agent's intelligence is strictly bounded by the explicit text, chapters, and knowledge contained within your uploaded PDF library.

## 🚀 Technical Stack

- **Orchestration & State Machine:** `langgraph` (Explicit Node & Edge execution topology)
- **LLM & Tool Binding Abstractions:** `langchain-core` / `langchain-openai`
- **Vector Infrastructure:** `Qdrant` (Running via local Docker container for high-performance semantic storage)
- **API Framework:** `FastAPI` (Asynchronous endpoints supporting live execution streaming)

---

## 📐 Architecture Flow

The system operates as a State Machine Graph (`StateGraph`), evaluating queries against a strict local topology:

1. **User Input:** Accepts queries alongside a unique `thread_id` to persist chat history across interactions.
2. **Agent/Router Node:** Evaluates the user query using structured JSON Tool Calling schemas to determine which books or chapters to scan.
3. **Local Retrieval Node:** Performs cosine similarity lookups over dense book vectors stored in Qdrant. Returns high-density parent chunks bundled with strict metadata tracking (Title, Chapter, Page).
4. **Consolidation & Generation Node:** Merges the local `context_pool` with active thread messages, feeding an advanced Academic Synthesizer prompt to generate the streaming output. If no information is found in the local library, the agent safely reports the absence of data rather than hallucinating.

---

## 🗂️ Project Scaffolding

```text
├── app/
│   ├── api/             # FastAPI routing layers and endpoints
│   ├── core/            # Core Agent Engine (graph.py, state.py, prompts.py)
│   ├── database/        # Connection setups and structural schemas
│   ├── tools/           # Custom tool handlers (vector_db.py)
│   └── config.py        # Environment variables type validation
├── scripts/
│   └── ingest.py        # High-density PDF chunking and indexing script
├── .env                 # Local secrets and API credentials storage
├── plan.md              # Technical execution step-by-step checklist
└── pyproject.toml       # Environment lock and dependency manifest
```

---

## 🛠️ Getting Started

### 1. Clone & Environment Configuration

Clone the repository and set up your Python virtual environment:

```bash
git clone <your-repository-url>
cd book-agentic-rag

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # Or use your preferred package manager (uv/poetry)
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key_here
QDRANT_URL=http://localhost:6333
```

### 3. Spin Up Vector Database

Launch the local Qdrant container:

```bash
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

Access the native web dashboard instantly at [http://localhost:6333/dashboard](http://localhost:6333/dashboard).

### 4. Run Textbook Ingestion

Place your technical PDFs in your data folder and index them into Qdrant:

```bash
python scripts/ingest.py
```

### 5. Launch the Server

Boot the FastAPI application backend:

```bash
uvicorn app.main:app --reload
```

---

## 🎯 Key Design Implementations (Built by Hand)

### Small-to-Big Chunking

Eliminates LLM context fragmentation. The vector database indexes optimized, short text pieces (~200 tokens) to achieve maximum retrieval accuracy, while the custom tool extracts the full surrounding Parent Chunk (~1200 tokens) to provide rich context to the prompt window.

### Strict Bounded Knowledge

No external search engine web hooks. The agent is strictly instructed to evaluate only the injected contexts, ensuring zero external hallucinations and complete information privacy.

### Metadata Slicing

Ingested books are indexed with explicit layer tokens (`book_title`, `chapter_number`, `page`). This permits programmatic context slicing based on conversational constraints.

---

## 📄 License

This project is licensed under the MIT License.
