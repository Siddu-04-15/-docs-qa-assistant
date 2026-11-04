
import json
from pathlib import Path
from typing import List, Dict

from app.ingestion.chunking import chunk_all_docs


# Locate docs.json relative to this Python file
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "docs.json"
)


def load_docs(path: Path = DATA_FILE) -> List[Dict]:
    """
    Load documents from the JSON dataset.
    """

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    docs = data.get("docs", [])

    if not isinstance(docs, list):
        raise ValueError("The 'docs' field must contain a list")

    for doc in docs:
        required_fields = ["doc_id", "title", "content"]

        for field in required_fields:
            if field not in doc:
                raise ValueError(
                    f"Document is missing required field: {field}"
                )

        if not isinstance(doc["content"], str):
            raise ValueError(
                f"Document content must be text: {doc['doc_id']}"
            )

    return docs


def prepare_chunks() -> List[Dict]:
    """
    Load documents and split them into chunks.
    """

    docs = load_docs()

    chunks = chunk_all_docs(docs)

    print(f"Documents loaded: {len(docs)}")
    print(f"Total chunks generated: {len(chunks)}")

    return chunks
