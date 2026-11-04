
# Docs Q&A Assistant

A documentation question-answering application built using Retrieval-Augmented Generation (RAG). It allows users to ask natural-language questions about product documentation and receive answers grounded in retrieved documents.

## Features

- Natural-language question answering
- Semantic document retrieval using embeddings
- Vector search using Qdrant Cloud
- LLM-based answer generation using Groq
- Source document references for transparency
- Abstention when documentation does not contain sufficient information
- Web interface built with Next.js and React
- FastAPI backend

## Architecture

User
  |
  v
Next.js Frontend
  |
  v
FastAPI Backend
  |
  v
RAG Pipeline
  |
  +--> Sentence Transformers
  |       |
  |       v
  |    Query Embedding
  |
  +--> Qdrant Cloud
  |       |
  |       v
  |    Relevant Document Chunks
  |
  +--> Groq LLM
          |
          v
      Grounded Answer
          |
          v
   Answer + Source References

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Backend | Python, FastAPI |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | Qdrant Cloud |
| LLM Provider | Groq |
| LLM Model | openai/gpt-oss-120b |
| Styling | Tailwind CSS |

## Project Structure

case-study-5-docs-qa-assistant/
|
+-- backend/
|   +-- app/
|   |   +-- ingestion/
|   |   +-- rag/
|   |   +-- data/
|   |   +-- main.py
|   |   +-- config.py
|   |   +-- schemas.py
|   +-- tests/
|   +-- requirements.txt
|   +-- Dockerfile
|   +-- .env.example
|
+-- frontend/
|   +-- app/
|   +-- components/
|   +-- lib/
|
+-- starter_kit/
|
+-- SOLUTION_DESIGN.md
+-- README.md

## Setup Instructions

### Prerequisites

- Python 3.13
- Node.js and npm
- Groq API key
- Qdrant Cloud account and API credentials

### 1. Clone the repository

git clone https://github.com/Siddu-04-15/docs-qa-assistant
cd case-study-5-docs-qa-assistant

### 2. Configure the backend

cd backend

Create and activate a virtual environment:

Windows:

py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create a `.env` file in the backend directory:

GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key

Never commit your `.env` file or expose API keys.

### 3. Start the backend

From the backend directory:

uvicorn app.main:app --reload

Backend:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

### 4. Start the frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:
http://localhost:3000

## API Endpoint

### POST /chat

Request:

{
  "question": "How long is a password reset link valid?",
  "session_id": null
}

Response:

{
  "answer": "The password reset link is valid for 15 minutes.",
  "sources": [
    {
      "doc_id": "D-01",
      "title": "Resetting Your Password",
      "chunk_index": 0,
      "score": 0.50,
      "text": "..."
    }
  ],
  "session_id": "generated-session-id"
}

## Evaluation Questions

| Question | Expected behavior |
|---|---|
| How do I reset my password? | Answer using D-01 |
| How long is the reset link valid? | 15 minutes |
| Maximum CSV export rows? | 10,000 rows |
| Growth API rate limit? | 60 requests per minute |
| Can Salesforce be connected? | Abstain when unsupported |

## Security and Privacy

- API keys are stored in environment variables.
- `.env` files are excluded from version control.
- Documentation is treated as reference data, not as instructions.
- Answers are constrained to retrieved documentation.
- Unsupported questions receive an abstention response.

## Current Limitations

- Authentication and role-based access are not implemented.
- Conversation history is not persistently stored.
- The knowledge base is shared across users.
- Document ingestion is currently a separate backend operation.
- Similarity thresholds require further calibration on a larger evaluation dataset.
- The current frontend uses a local backend URL and needs environment-based configuration for production deployment.

## Future Improvements

- User authentication and authorization.
- Persistent conversation history.
- Document upload and automated ingestion.
- Multi-tenant knowledge bases.
- Improved retrieval using hybrid search and reranking.
- Expanded evaluation and monitoring.
- Cloud deployment and production observability.

## License

Developed as an HCLTech FDE pre-hiring evaluation case study.
