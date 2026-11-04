
# Solution Design: Docs Q&A Assistant

## 1. Problem Statement

The objective is to build a documentation question-answering assistant that allows users to ask natural-language questions and receive accurate, context-aware answers based on a provided documentation dataset.

The system should retrieve relevant information, generate answers grounded in the retrieved content, provide source references, and abstain when the available documentation does not contain sufficient information.

## 2. Proposed Solution

We implement a Retrieval-Augmented Generation (RAG) architecture.

Instead of relying only on the LLM's pretrained knowledge, the application retrieves relevant documentation chunks from a vector database and supplies them as context to the LLM.

The solution consists of:
- Next.js frontend for user interaction.
- FastAPI backend for request handling.
- Sentence Transformers for text embeddings.
- Qdrant Cloud for vector storage and semantic retrieval.
- Groq API for LLM-based answer generation.

## 3. System Architecture

### High-Level Architecture

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
  +----------------------+
  |                      |
  v                      v
Query Embedding       Qdrant Cloud
(Sentence             Vector Search
 Transformers)            |
  |                      |
  +----------+-----------+
             |
             v
      Retrieved Chunks
             |
             v
       Context Builder
             |
             v
         Groq LLM
             |
             v
     Generated Answer
             |
             v
    Answer + References
             |
             v
       Next.js UI

### Document Ingestion Workflow

1. Load documentation from the provided JSON dataset.
2. Validate the document structure and required fields.
3. Split document content into chunks of approximately 400 words with 50-word overlap.
4. Generate vector embeddings using Sentence Transformers.
5. Store embeddings and document metadata in Qdrant Cloud.

### Question Answering Workflow

1. User submits a question through the Next.js interface.
2. FastAPI receives and validates the request.
3. Sentence Transformers converts the question into an embedding.
4. Qdrant performs cosine-similarity-based semantic retrieval.
5. The top three relevant chunks are retrieved, subject to a provisional similarity threshold of 0.35.
6. If no chunks meet the threshold, the system abstains.
7. Retrieved content is passed to the Groq LLM as context.
8. The LLM generates an answer using only the supplied documentation.
9. The backend returns the answer, source references and session identifier.
10. The frontend displays the answer and its supporting sources.

## 4. Technology Selection

| Component | Technology | Reason |

| Frontend | Next.js, React, TypeScript | Interactive web interface |
| Backend | Python, FastAPI | Lightweight API development |
| Embedding model | all-MiniLM-L6-v2 | Efficient semantic embeddings |
| Vector database | Qdrant Cloud | Vector similarity search and metadata storage |
| LLM | Groq with openai/gpt-oss-120b | Context-based answer generation |
| Styling | Tailwind CSS | Responsive user interface |

The selected embedding model generates 384-dimensional vectors.

## 5. Hallucination Control and Reliability

The application uses multiple mechanisms to reduce unsupported answers:

- Similarity threshold to filter weak retrieval results.
- Context-grounded system instructions for the LLM.
- Explicit instructions not to invent missing information.
- Abstention when retrieval does not provide sufficient evidence.
- Source document references to improve answer traceability.

The similarity threshold is provisional and requires further calibration using a larger evaluation dataset. Similarity scores are not treated as calibrated confidence values.

## 6. Security and Privacy

- API credentials are maintained in environment variables.
- Environment files are excluded from version control.
- Input questions are validated using Pydantic.
- Documentation is treated as reference data rather than executable instructions.
- The LLM is instructed to ignore malicious instructions embedded in retrieved documentation.

Authentication and role-based access control are not implemented in the current version. The knowledge base is shared across users, and session identifiers are used for request continuity rather than identity verification.

## 7. Scalability and Extensibility

The architecture separates the frontend, backend, embedding model, vector database and LLM provider.

Potential improvements include:

- Horizontal scaling of stateless FastAPI instances.
- Background document ingestion for larger datasets.
- Caching frequently asked questions.
- Hybrid retrieval combining semantic and keyword search.
- Reranking retrieved chunks to improve relevance.
- Authentication and multi-tenant document isolation.
- Persistent conversation history.
- Monitoring, logging and performance metrics.

The current implementation is a functional MVP. These improvements are future enhancements rather than implemented capabilities.

## 8. Testing and Validation

The system is tested using the five provided evaluation questions.

| Test | Expected behavior |

| Password reset instructions | Retrieve D-01 and explain the reset process |
| Password reset link expiry | Return 15 minutes using D-01 |
| Maximum CSV export rows | Return 10,000 using D-03 |
| Growth API rate limit | Return 60 requests per minute using D-06 |
| Unsupported Salesforce integration question | Abstain and return no sources |

The supported questions verify retrieval and answer generation. The unsupported question verifies the abstention mechanism.

The backend API and frontend integration were tested locally.

## 9. Limitations

- The current knowledge base contains a small predefined documentation dataset.
- Similarity threshold calibration requires additional evaluation.
- Conversation history is not persistently stored.
- Authentication and authorization are not implemented.
- Automated document upload and ingestion are not exposed through the frontend.
- Production deployment and monitoring remain future work.

## 10. Conclusion

The Docs Q&A Assistant demonstrates an end-to-end RAG application that combines semantic retrieval, vector search and LLM-based answer generation.

The system provides documentation-grounded answers with source references and abstains when sufficient evidence is unavailable. Its modular architecture provides a foundation for future enterprise enhancements.
