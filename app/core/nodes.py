import json
from app.core.llm import llm
from app.core.prompts import ROUTER_SYSTEM_PROMPT, ROUTER_HUMAN_PROMPT
from app.core.prompts import GENERATION_SYSTEM_PROMPT, GENERATION_HUMAN_PROMPT
from app.core.state import GraphState
from app.database.vector_store import client, store


collection_name = "books"


def router_node(state: GraphState) -> dict:
    # 1. Get list of available books from Qdrant
    points, _ = client.scroll(
        collection_name="books",
        limit=1000,
        with_payload=["book_title"],
        with_vectors=False,
    )
    available = list(set(p.payload["book_title"] for p in points if p.payload.get("book_title")))

    # 2. Call OpenCode and parse JSON manually
    messages = [
        ("system", ROUTER_SYSTEM_PROMPT + "\n\nRespond ONLY with a valid JSON in the format: {\"book_title\": \"...\" or null, \"rationale\": \"...\"}"),
        ("human", ROUTER_HUMAN_PROMPT.format(
            available_books=", ".join(available),
            question=state["question"]
        )),
    ]

    result = llm.invoke(messages)
    parsed = json.loads(result.content)
    return {"selected_book": parsed["book_title"]}


def retrieval_node(state: GraphState) -> dict:
    if not state["selected_book"]:
        return {"context_pool": []}

    results = store.query(state["selected_book"], state["question"])
    return {"context_pool": [r.payload for r in results]}


def generation_node(state: GraphState) -> dict:
    xml_context = "\n".join(
        f'<chunk book="{c["book_title"]}" page="{c["page"]}">{c["text"]}</chunk>'
        for c in state["context_pool"]
    )

    messages = [
        ("system", GENERATION_SYSTEM_PROMPT),
        ("human", GENERATION_HUMAN_PROMPT.format(
            context_pool=xml_context,
            question=state["question"]
        )),
    ]

    answer = llm.invoke(messages)
    return {"answer": answer.content}
