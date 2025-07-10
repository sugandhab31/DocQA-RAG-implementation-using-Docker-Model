import os
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

FAISS_INDEX_PATH = "vectorstore/faiss_index.index"
CHUNKS_PATH = "vectorstore/chunks.pkl"

def split_text(text: str, chunk_size: int = 500) -> List[str]:
    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def create_vectorstore(chunks: List[str]):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    return f"Vectorstore created with {len(chunks)} chunks."

def retrieve_similar_chunks(query: str, top_k: int=3)-> List[str]:
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = [chunks[i] for i in indices[0]]

    return results