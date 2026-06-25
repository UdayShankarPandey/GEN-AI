# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

# bge-large-en-v1.5: ~1.34 GB, 1024-dim vectors
# Top-quality English embedding model (MTEB leaderboard)
# BGE models require normalize_embeddings=True for correct cosine similarity scores
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": "cpu", "trust_remote_code": True},
    encode_kwargs={"normalize_embeddings": True},
)

# --- Single query embedding ---
query = "What is LangChain?"
query_vector = embeddings.embed_query(query)
print(f"Query embedding dim : {len(query_vector)}")
print(f"First 5 values      : {query_vector[:5]}")

# --- Batch document embeddings ---
docs = [
    "LangChain is a framework for building LLM applications.",
    "Groq provides ultra-fast LLM inference.",
    "FAISS is a library for efficient similarity search.",
]
doc_vectors = embeddings.embed_documents(docs)
print(f"\nEmbedded {len(doc_vectors)} documents")
print(f"Each vector dim: {len(doc_vectors[0])}")