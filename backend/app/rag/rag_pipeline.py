
from app.rag.retriever import retriever
from app.rag.llm import llm


class RAGPipeline:

    def __init__(self):
        self.retriever = retriever
        self.llm = llm

    def answer_question(self, question: str) -> dict:
        """
        Complete RAG workflow:
        1. Retrieve relevant documents.
        2. Check whether relevant evidence exists.
        3. Generate an answer using Groq.
        4. Return answer and source references.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        # Step 1: Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(question)

        # Step 2: Handle unsupported questions
        if not retrieved_docs:
            return {
                "answer": (
                    "I couldn't find sufficient information "
                    "in the available documentation to answer "
                    "your question."
                ),
                "sources": []
            }

        # Step 3: Prepare context for the LLM
        context_parts = []

        for doc in retrieved_docs:
            context_parts.append(
                f"""
Document ID: {doc['doc_id']}
Title: {doc['title']}
Content: {doc['text']}
"""
            )

        context = "\n".join(context_parts)

        # Step 4: Generate grounded answer
        answer = self.llm.generate_answer(
            question=question,
            context=context
        )

        # Step 5: Prepare source references
        sources = []

        for doc in retrieved_docs:
            sources.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "chunk_index": doc["chunk_index"],
                "score": doc["score"],
                "text": doc["text"]
            })

        return {
            "answer": answer,
            "sources": sources
        }


# Reusable RAG pipeline
rag_pipeline = RAGPipeline()
