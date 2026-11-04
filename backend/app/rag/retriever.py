
from app.config import settings
from app.rag.embeddings import embedding_model
from app.rag.vector_store import vector_store


class Retriever:

    def __init__(self):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(self, question: str, top_k: int = None):
        """
        Retrieve relevant document chunks using semantic search.
        Reject results below the relevance threshold.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        if top_k is None:
            top_k = settings.TOP_K

        # Step 1: Generate embedding for the user question
        query_vector = self.embedding_model.generate_embedding(
            question
        )

        # Step 2: Search for similar vectors in Qdrant
        search_result = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True
        )

        # Step 3: Filter and extract relevant document chunks
        results = []

        for point in search_result.points:

            payload = point.payload or {}

            # Apply similarity threshold
            if point.score < settings.SIMILARITY_THRESHOLD:
                continue

            results.append({
                "doc_id": payload.get("doc_id"),
                "title": payload.get("title"),
                "chunk_index": payload.get("chunk_index"),
                "text": payload.get("text"),
                "score": point.score
            })

        return results


# Create a reusable retriever instance
retriever = Retriever()
