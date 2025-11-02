import os
import torch
import chromadb
import shutil
import datetime
from paths import VECTOR_DB_DIR
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import load_all_documents
from keybert import KeyBERT


def initialize_db(
    persist_directory: str = VECTOR_DB_DIR,
    collection_name: str = "documents",
    delete_existing: bool = False,
) -> chromadb.Collection:
    """
    Initialize a ChromaDB instance and persist it to disk.

    Args:
        persist_directory (str): The directory where ChromaDB will persist data. Defaults to "./vector_db"
        collection_name (str): The name of the collection to create/get. Defaults to "publications"
        delete_existing (bool): Whether to delete the existing database if it exists. Defaults to False
    Returns:
        chromadb.Collection: The ChromaDB collection instance
    """
    if os.path.exists(persist_directory) and delete_existing:
        shutil.rmtree(persist_directory)

    os.makedirs(persist_directory, exist_ok=True)

    # Initialize ChromaDB client with persistent storage
    client = chromadb.PersistentClient(path=persist_directory)

    # Create or get a collection
    try:
        # Try to get existing collection first
        collection = client.get_collection(name=collection_name)
        print(f"Retrieved existing collection: {collection_name}")
    except Exception:
        # If collection doesn't exist, create it
        collection = client.create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine",
                "hnsw:batch_size": 10000,
            },  # Use cosine distance for semantic search
        )
        print(f"Created new collection: {collection_name}")

    print(f"ChromaDB initialized with persistent storage at: {persist_directory}")

    return collection


def get_db_collection(
    persist_directory: str = VECTOR_DB_DIR,
    collection_name: str = "documents",
) -> chromadb.Collection:
    """
    Get a ChromaDB client instance.

    Args:
        persist_directory (str): The directory where ChromaDB persists data
        collection_name (str): The name of the collection to get

    Returns:
        chromadb.PersistentClient: The ChromaDB client instance
    """
    return chromadb.PersistentClient(path=persist_directory).get_collection(
        name=collection_name
    )


def chunk_document(
    document: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> list[str]:
    """
    Chunk the document into smaller documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_text(document)


def embed_documents(documents: list[str]) -> list[list[float]]:
    """
    Embed documents using a model.
    """
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": device},
    )

    embeddings = model.embed_documents(documents)
    return embeddings


def extract_keywords(text, n=3):
    kw_model = KeyBERT(model="all-MiniLM-L6-v2")
    keywords = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 1), stop_words="english", top_n=n
    )
    # Return only the keyword strings
    return [kw[0] for kw in keywords]


def insert_documents(collection: chromadb.Collection, documents: list[str]):
    next_id = collection.count()
    for i, document in enumerate(documents):
        # Extract metadata using document content only
        doc_metadata = {
            "source": f"document_{next_id + i}",
            "title": document.split("\n")[0][
                :100
            ],  # First line or first 100 chars as title
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),  # Use current date
            "tags": ", ".join(extract_keywords(document, n=3)),
        }
        chunked_document = chunk_document(document)
        embeddings = embed_documents(chunked_document)
        ids = [f"document_{next_id + j}" for j in range(len(chunked_document))]
        metadatas = [
            {**doc_metadata, "chunk_index": j, "length": len(chunk)}
            for j, chunk in enumerate(chunked_document)
        ]
        collection.add(
            embeddings=embeddings,
            ids=ids,
            documents=chunked_document,
            metadatas=metadatas,
        )
        next_id += len(chunked_document)


def main():
    collection = initialize_db(
        persist_directory=VECTOR_DB_DIR,
        collection_name="documents",
        delete_existing=True,
    )
    documents = load_all_documents()
    insert_documents(collection, documents)

    print(f"Total documents in collection: {collection.count()}")


if __name__ == "__main__":
    main()
