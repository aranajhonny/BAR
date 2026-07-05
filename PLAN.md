# PLAN — BAR as a learning vehicle

This document isn't a product roadmap. It's a log of what I want to understand about LangChain, LangGraph, and Python by building something real, in the order it makes sense to learn it. Each phase has a comprehension goal, not just a feature.

## Why this project instead of a tutorial

Copying a RAG tutorial teaches you to paste blocks of code that already work. This project is meant to run the other way: pick a closed domain (my own technical books) where I can actually notice when retrieval fails, when the router picks wrong, and why — because I know the content by heart and can audit every answer against the original text.

## Phase 0 — Foundations already running

- [x] Basic `StateGraph` with three nodes (Router → Retrieval → Generation)
- [x] PDF ingestion with small-to-big chunking
- [x] Local Qdrant with metadata (`book_title`, `chapter_number`, `page`)
- [x] Streamed response via FastAPI

## Phase 1 — Actually understanding LangGraph, not just using it

- [ ] Write the end-to-end smoke test (query → retrieval → generation) *before* adding any more nodes. Without this, every change to the graph is a guess.
- [ ] Instrument each node with input/output state logging — I want to *see* what the Router decides and why, not assume it.
- [ ] Deliberately provoke a case where the Router picks the wrong book/chapter, and figure out whether it's a prompt problem, a schema problem, or poor metadata.
- [ ] Read the actual source of `langgraph.graph.StateGraph` (not just the docs) to understand how state propagates between nodes — it's the piece I understand least right now.

## Phase 2 — Retrieval, beyond "it works"

- [ ] Measure retrieval precision against a small set of questions with known answers (I build the ground truth myself, since I know the books).
- [ ] Experiment with chunk size (200 → 100 → 400 tokens) and see the real, not theoretical, impact on answer quality.
- [ ] Try reranking (cross-encoder) after the cosine search, and decide with data whether the extra complexity is worth it.

## Phase 3 — Real conversational memory

- [ ] Persist `thread_id` using LangGraph's native checkpointing (`MemorySaver` → later a persistent backend) instead of rebuilding history by hand.
- [ ] Understand the difference between graph state and conversation memory — LangGraph blends the two, and I want to separate them clearly in my head.

## Phase 4 — Getting off the OpenAI dependency (optional, curiosity-driven)

- [ ] Swap embeddings for a local model (e.g. `bge-small` via `sentence-transformers`) and compare retrieval quality against `text-embedding-3-small`.
- [ ] Try a local LLM via Ollama for generation, and measure where the quality gap actually shows up on longer answers.
- [ ] If this works well, the "100% local" label stops being aspirational.

## Phase 5 — Things I want to break on purpose

- [ ] Feed in a PDF that contradicts another book in the library and see how the agent handles (or doesn't handle) the contradiction.
- [ ] Ask something outside the library and confirm the system admits "I don't know" instead of hallucinating — this is the project's core honesty test.
- [ ] Push a very long thread and see where context handling degrades.

## Notes to self

- Don't add a new feature without writing the test that validates it first. I already did this with Vlk² — documented capabilities the code didn't back up — and I want the opposite habit here from day one.
- This README and this plan should always state the true current status of the code, even when it's less impressive. The goal is learning, not selling myself the project.
- If at any point this stops feeling like learning and starts feeling like a race toward a roadmap, that's a sign I'm fooling myself about what this repo is for.
