from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


DOCUMENTS_PATH = "documents"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "devops_knowledge"

# 1. Load Markdown documents
loader = DirectoryLoader(
    DOCUMENTS_PATH,
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)

documents = loader.load()

print(f"Loaded documents: {len(documents)}")

# 2. Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)

chunks = text_splitter.split_documents(documents)

print(f"Created chunks: {len(chunks)}")

# 3. Create embeddings using Ollama
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

# 4. Store embeddings in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url=QDRANT_URL,
    collection_name=COLLECTION_NAME,
)

print("Documents successfully stored in Qdrant.")

