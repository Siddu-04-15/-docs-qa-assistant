
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    # Application
    APP_NAME: str = "Docs Q&A Assistant"

    # Groq API credentials
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Qdrant credentials
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Vector database
    COLLECTION_NAME: str = "docs_qa_collection"

    # Embedding model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # Text chunking
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50

    # Retrieval
    TOP_K: int = 3

    # Retrieval relevance threshold (initial value)
    SIMILARITY_THRESHOLD: float = 0.35

    GROQ_MODEL: str = "openai/gpt-oss-120b"

settings = Settings()
