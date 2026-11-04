
from app.rag.retriever import retriever


questions = [
    "How long is a password reset link valid?",
    "What is the maximum number of rows I can export to CSV?",
    "What is the API rate limit for Growth users?",
    "Can Salesforce be connected?"
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:", question)

    results = retriever.retrieve(question)

    if not results:
        print("No sufficiently relevant documentation found.")
        continue

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Document ID:", result["doc_id"])
        print("Title:", result["title"])
        print("Similarity Score:", round(result["score"], 4))
        print("Text:", result["text"])
