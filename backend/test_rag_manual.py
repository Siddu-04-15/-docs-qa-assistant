
from app.rag.rag_pipeline import rag_pipeline


questions = [
    "How long is a password reset link valid?",
    "What is the maximum number of rows I can export to CSV?",
    "What is the API rate limit for Growth users?",
    "Can Salesforce be connected?"
]


for question in questions:

    print("\n" + "=" * 75)
    print("QUESTION:", question)

    result = rag_pipeline.answer_question(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['doc_id']}: "
            f"{source['title']} "
            f"(Score: {source['score']:.4f})"
        )
