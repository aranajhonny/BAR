# Execution Plan: Book-Agentic-RAG (From Scratch)

This document serves as the step-by-step roadmap for building a modular, agentic RAG backend specialized in technical PDF books. Built from scratch using Python, FastAPI, LangGraph, LangChain, and Qdrant (Docker), this architecture emphasizes manual control and deterministic orchestration over high-level abstractions.

---

## 🛠️ Phase 1: Environment, Base Architecture & API Server
The goal is to set up the project scaffolding, environment isolation, and basic communication endpoints without any agentic logic yet.

- [ ] **Step 1.1: Workspace Initialization**
  - Create the modular directory structure: `app/core`, `app/tools`, `app/api`, and `scripts/`.
  - Configure the virtual environment using your preferred package manager (`uv` or `poetry`).
  - Install core dependencies: `fastapi`, `uvicorn`, `langgraph`, `langchain-core`, `langchain-openai`, `pydantic`, `python-dotenv`.
- [ ] **Step 1.2: Configuration & Environment Isolation**
  - Create a `.env` file to securely store `OPENAI_API_KEY`, `EXA_API_KEY`, and `QDRANT_URL`.
  - Code `app/config.py` using `pydantic-settings` or native `os.environ` to type-check and validate credentials at application startup.
- [ ] **Step 1.3: Base Endpoints with FastAPI**
  - Write `app/main.py` and instantiate the FastAPI application.
  - Design the Pydantic schema for the incoming payload (e.g., `{"message": "...", "thread_id": "..."}`).
  - Implement an asynchronous `POST /v1/chat` endpoint that initially returns a generic JSON confirmation.

---

## 📚 Phase 2: High-Density Ingestion (RAG Pipeline for Books)
Processing extensive textbooks requires strict token context management and highly structured metadata extraction by chapter and section.

- [ ] **Step 2.1: Vector Infrastructure Setup**
  - Spin up a local Qdrant instance via Docker (`docker run -p 6333:6333...`).
  - Access the Qdrant Web Dashboard (port 6333) to verify the service is up and running.
- [ ] **Step 2.2: Extensible Extraction & Ingestion Script (`scripts/ingest.py`)**
  - Program the PDF parser to process files in page-batches (using `PyMuPDF` or `pdfplumber`) to avoid RAM bottlenecks.
  - Implement a *Hierarchical Chunking* or *Small-to-Big Chunking* strategy:
    - Generate granular sub-chunks (~200-300 tokens) for sharp semantic vector matching.
    - Map each sub-chunk explicitly to a "Parent Chunk" (~1000-1200 tokens) that contains the broader surrounding context.
  - Inject mandatory structured metadata into every vector payload: `book_title`, `chapter_number`, `chapter_title`, `page_start`, `page_end`.
- [ ] **Step 2.3: Strict Retrieval Module**
  - Write `app/tools/vector_db.py`.
  - Create an asynchronous query function that connects to the Qdrant collection, runs a cosine similarity search, and returns only the clean "Parent Chunks" paired with their source metadata.

---

## 🧠 Phase 3: State, Tools & LLM Binding
Configuring the atomic components that your graph orchestrator will explicitly manipulate.

- [ ] **Step 3.1: Central State Definition (`app/core/state.py`)**
  - Design the graph state structure inheriting from `TypedDict`.
  - Define mandatory keys for the execution's short-term memory:
    - `messages`: A cumulative list managing the chronological conversation flow (`list[BaseMessage]`).
    - `context_pool`: A list of structured dictionaries where retrieval nodes will store fetched book passages or web results.
- [ ] **Step 3.2: Tool Encapsulation**
  - Wrap the Qdrant retrieval function under LangChain's `@tool` decorator, writing an exhaustive docstring explaining exactly when the LLM should invoke it.
  - Create `app/tools/web_search.py` wrapping the `Exa` or `Tavily` API with strict filters to restrict external queries to academic or engineering sources if local vector data falls short.
- [ ] **Step 3.3: Binding LLMs to Tool Schemas**
  - In `app/core/graph.py`, initialize the OpenAI Chat Model.
  - Use the `.bind_tools([...])` method, passing your hand-coded tools list to enable deterministic Tool Calling via structured JSON responses.

---

## 🕸️ Phase 4: Deterministic Graph Orchestration (LangGraph Core)
Wiring the standalone python functions into a controlled state-machine loop.

- [ ] **Step 4.1: Hand-Coding Independent Nodes**
  - **Router/Agent Node:** Passes the current state messages to the LLM with bound tools, saving the response (including potential `tool_calls`) back to the state.
  - **Tools Execution Node:** Reads the state, extracts requested tool calls, executes the respective functions (Qdrant or Web) concurrently, and commits clean results to the `context_pool`.
  - **Final Generator Node:** Gathers all accumulated `context_pool` data and `messages`, injects them into a strict "Academic Book Assistant" system prompt (`app/core/prompts.py`), calls the LLM for the final answer, and flushes the context pool.
- [ ] **Step 4.2: Conditional Edge Logic**
  - Write the routing decision function (`should_continue`). This inspects the latest agent message inside the state:
    - If it contains `tool_calls`, it routes directly to the tools execution node.
    - If no tool calls are present, it transitions to the final generator node to close the loop.
- [ ] **Step 4.3: Graph Assembly & Compilation**
  - Instantiate `StateGraph(YourStateSchema)`.
  - Register nodes explicitly via `.add_node()`.
  - Wire the flow using `.add_edge()` for fixed transitions and `.add_conditional_edges()` for branching logic based on `should_continue`.
  - Set the primary entry point via `.set_entry_point()`.
  - Compile the graph layout by calling `.compile()`.

---

## 💾 Phase 5: Persistence Layer, Streaming & API Integration
Connecting the core engine with the web interface to support persistent sessions and multi-user chat threads.

- [ ] **Step 5.1: Memory Saver Checkpointer**
  - Import and instantiate LangGraph's native `MemorySaver`.
  - Pass the checkpointer instance during graph compilation to ensure state persistence in RAM indexed by session IDs.
- [ ] **Step 5.2: Final Wiring in FastAPI**
  - Update the endpoint created in Phase 1 (`app/main.py`).
  - Import the compiled graph and call it asynchronously using `.astream()` or `.ainvoke()`.
  - Configure the execution context payload: `config={"configurable": {"thread_id": payload.thread_id}}` to guarantee complete session isolation.
- [ ] **Step 5.3: Manual Integration Testing**
  - Launch the local development server (`uvicorn app.main:app --reload`).
  - Use an HTTP client to fire sequential, complex queries to test conversation memory retention and deterministic tool switching between book lookups and web searches.
