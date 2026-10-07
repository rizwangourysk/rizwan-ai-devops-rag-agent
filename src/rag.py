from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "devops_knowledge"


# 1. Embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Connect to Qdrant
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
)


# 3. Load Qwen LLM
llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0,
)


# 4. Get user question
question = input("Enter your DevOps question: ")


# 5. Search Qdrant
results = vector_store.similarity_search(
    question,
    k=3,
)


# 6. Combine retrieved information
context = "\n\n".join(
    document.page_content
    for document in results
)


# 7. Create prompt for the LLM
prompt = f"""
You are an AI DevOps troubleshooting assistant.

Answer the user's question using the provided DevOps knowledge.

If the information is not available in the knowledge,
clearly say that the information is not available.

DevOps Knowledge:
{context}

User Question:
{question}

Give a simple and practical answer.
Include useful kubectl or Docker commands when available.
"""


# 8. Ask Qwen
response = llm.invoke(prompt)


# 9. Print final answer
print("\n--- AI DevOps Answer ---\n")
print(response.content)
