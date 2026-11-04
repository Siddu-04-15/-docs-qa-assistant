
import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse
from app.rag.rag_pipeline import rag_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Docs Q&A Assistant",
    description="A RAG-based documentation question-answering application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Docs Q&A Assistant API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = rag_pipeline.answer_question(request.question)

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            session_id=request.session_id or str(uuid4())
        )

    except Exception:
        logger.exception("Error while processing chat request")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your question."
        )
