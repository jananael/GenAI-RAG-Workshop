import chromadb
from app.rag.embeddings import embed_text

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="documents")

def add_documents(texts: list[str]):
    embeddings = [embed_text(t) for t in texts]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(texts))]
    )

def query_documents(query: str, n_results: int = 3):
    query_emb = embed_text(query)
    return collection.query(
        query_embeddings=[query_emb],
        n_results=n_results
    )
