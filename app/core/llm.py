from langchain_openai import ChatOpenAI
from app.config import settings

llm = ChatOpenAI(
    model=settings.OPENCODE_MODEL,
    api_key=settings.OPENCODE_API_KEY,
    base_url="https://opencode.ai/zen/go/v1",
)
