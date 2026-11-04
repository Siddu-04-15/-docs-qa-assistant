
from app.rag.embeddings import embedding_model

# Sample documentation text
text = "Password reset links expire after 15 minutes."

# Generate embedding
vector = embedding_model.generate_embedding(text)

print("Embedding generated successfully!")
print("Vector dimensions:", len(vector))
print("First 10 values:", vector[:10])
