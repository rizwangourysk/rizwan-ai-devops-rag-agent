from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "devops_knowledge"

# Create the same embedding model used during ingestion
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Connect to existing Qdrant collection
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
)

question = input("Enter your DevOps question: ")

# Search for the 3 most relevant chunks
results = vector_store.similarity_search(
    question,
    k=3,
)

print("\n--- Retrieved Information ---\n")

for i, document in enumerate(results, start=1):
    print(f"Result {i}:")
    print(document.page_content)
    print("-" * 60)
