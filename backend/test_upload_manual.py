
from app.ingestion.ingest import prepare_chunks
from app.rag.embeddings import embedding_model
from app.rag.vector_store import vector_store


def upload_documents():

    print("\nLoading documents...")
    chunks = prepare_chunks()

    print("\nGenerating embeddings...")
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.generate_embeddings(texts)

    print("\nUploading vectors to Qdrant...")
    vector_store.upsert_chunks(chunks, embeddings)

    print("\nVerifying uploaded data...")

    info = vector_store.client.get_collection(
        collection_name=vector_store.collection_name
    )

    print("Total vectors stored:", info.points_count)
    print("\nDocument ingestion completed successfully!")


if __name__ == "__main__":
    upload_documents()
