from typing import TypedDict

class GraphState(TypedDict):
    question: str
    thread_id: str
    selected_book: str | None
    context_pool: list[dict]
    answer: str
