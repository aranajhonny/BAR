from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.graph import graph

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    thread_id: str


@router.post("/query")
async def query(request: QueryRequest):
    initial_state = {
        "question": request.question,
        "thread_id": request.thread_id,
        "selected_book": None,
        "context_pool": [],
        "answer": "",
    }

    result = graph.invoke(initial_state)

    return {"answer": result["answer"]}
