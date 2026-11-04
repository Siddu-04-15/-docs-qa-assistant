
from app.ingestion.ingest import load_docs, prepare_chunks

docs = load_docs()
chunks = prepare_chunks()

print("\nFirst document:")
print(docs[0]["title"])

print("\nFirst generated chunk:")
print(chunks[0])
