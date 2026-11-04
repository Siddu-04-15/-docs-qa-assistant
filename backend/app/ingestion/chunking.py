
from typing import List, Dict

from app.config import settings


def chunk_text(
    text: str,
    chunk_size: int = settings.CHUNK_SIZE,
    overlap: int = settings.CHUNK_OVERLAP
) -> List[str]:
    """
    Split text into overlapping chunks using whitespace tokens.
    Short documents are returned as a single chunk.
    """

    words = text.split()

    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    if len(words) <= chunk_size:
        return [text.strip()]

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


def chunk_all_docs(
    docs: List[Dict]
) -> List[Dict]:
    """
    Split all documents and preserve their metadata.
    """

    all_chunks = []

    for doc in docs:
        text_chunks = chunk_text(doc["content"])

        for idx, chunk in enumerate(text_chunks):
            all_chunks.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "chunk_index": idx,
                "text": chunk
            })

    return all_chunks
