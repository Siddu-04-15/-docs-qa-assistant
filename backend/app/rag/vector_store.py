
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
from uuid import uuid5, NAMESPACE_DNS

from app.config import settings


class VectorStore:

    def __init__(self):
        if not settings.QDRANT_URL or not settings.QDRANT_API_KEY:
            raise ValueError(
                "QDRANT_URL and QDRANT_API_KEY must be configured"
            )

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )

        self.collection_name = settings.COLLECTION_NAME

    def create_collection(self):
        """
        Create a Qdrant collection if it doesn't exist.
        """

        if not self.client.collection_exists(
            collection_name=self.collection_name
        ):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )

            print("Qdrant collection created successfully!")

        else:
            print("Qdrant collection already exists.")

    def upsert_chunks(self, chunks: list, embeddings: list):
        """
        Store document chunks and their embeddings in Qdrant.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match"
            )

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            if len(embedding) != settings.EMBEDDING_DIMENSION:
                raise ValueError("Invalid embedding dimensions")

            point_id = str(uuid5(
                NAMESPACE_DNS,
                f"{chunk['doc_id']}_{chunk['chunk_index']}"
            ))

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "doc_id": chunk["doc_id"],
                        "title": chunk["title"],
                        "chunk_index": chunk["chunk_index"],
                        "text": chunk["text"]
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True
        )

        print(f"Successfully stored {len(points)} chunks in Qdrant!")


# Reusable vector store instance
vector_store = VectorStore()
