
from app.rag.llm import llm


question = "How long is a password reset link valid?"

context = """
Password reset links expire after 15 minutes.
If a link expires, return to the login page
and request a brand new reset link.
"""

print("Question:", question)

print("\nGenerating answer...\n")

answer = llm.generate_answer(
    question=question,
    context=context
)

print("LLM Answer:")
print(answer)
