
from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def generate_embedding(self, text: str) -> list:
        """
        Convert a single text into a vector.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    def generate_embeddings(self, texts: list) -> list:
        """
        Convert multiple texts into vectors.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings.tolist()


# Create a reusable embedding model
embedding_model = EmbeddingModel()
