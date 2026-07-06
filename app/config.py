import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENCODE_API_KEY: str = os.getenv("OPENCODE_API_KEY") or os.getenv("OPENROUTER_API_KEY", "")
    OPENCODE_MODEL: str = os.getenv("OPENCODE_MODEL", "deepseek-v4-flash")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")

    def __init__(self):
        if not self.OPENCODE_API_KEY:
            raise ValueError(
                "OPENCODE_API_KEY is not set. "
                "Create a .env file with OPENCODE_API_KEY=sk-... "
                "or export it in your shell."
            )
        if not self.QDRANT_URL:
            raise ValueError("QDRANT_URL is not set.")


settings = Settings()
