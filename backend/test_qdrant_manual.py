
from app.rag.vector_store import vector_store

try:
    # Test connection to Qdrant
    print("Connecting to Qdrant Cloud...")

    collections = vector_store.client.get_collections()

    print("\nConnection successful!")
    print("Available collections:")

    for collection in collections.collections:
        print("-", collection.name)

    # Create our collection
    print("\nCreating Docs Q&A collection...")
    vector_store.create_collection()

    # Verify collection
    info = vector_store.client.get_collection(
        collection_name=vector_store.collection_name
    )

    print("\nCollection verified!")
    print("Collection name:", vector_store.collection_name)
    print("Vector size:", info.config.params.vectors.size)
    print("Distance:", info.config.params.vectors.distance)

except Exception as e:
    print("\nQdrant connection failed!")
    print("Error:", str(e))
