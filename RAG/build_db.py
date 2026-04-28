from chunk_code import load_project
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# model embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# load code từ App của bạn
chunks = load_project("../App")

client = chromadb.Client(
    Settings(persist_directory="../Data/vector_db")
)

collection = client.get_or_create_collection("codebase")

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["code"]).tolist()

    collection.add(
        documents=[chunk["code"]],
        metadatas=[{
            "file": chunk["file"],
            "name": chunk["name"],
            "type": chunk["type"]
        }],
        ids=[str(i)],
        embeddings=[embedding]
    )

print("Done indexing!")