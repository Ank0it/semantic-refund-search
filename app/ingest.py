"""
Ingestion script for the Semantic Refund Search project.

Responsibilities:
- Load refund policy dataset
- Validate dataset
- Generate embeddings
- Store embeddings and metadata in ChromaDB
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Allow running this file directly:
# python app/ingest.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.config import (  # noqa: E402
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    DATASET_PATH,
    EMBEDDING_MODEL,
)


REQUIRED_FIELDS = {
    "id",
    "title",
    "category",
    "source",
    "text",
}


def load_dataset() -> list[dict]:
    """
    Load and validate the refund policy dataset.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Dataset must be a JSON array.")

    for index, item in enumerate(data, start=1):

        missing = REQUIRED_FIELDS - item.keys()

        if missing:
            raise ValueError(
                f"Entry {index} is missing fields: {missing}"
            )

    return data


def get_collection():
    """
    Create or load a persistent ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=str(CHROMA_DB_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def ingest_documents(
    dataset: list[dict],
    collection,
    model: SentenceTransformer,
) -> None:
    """
    Generate embeddings and store all documents.
    """

    print("\nGenerating embeddings...\n")

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for item in dataset:

        ids.append(item["id"])

        documents.append(item["text"])

        metadatas.append(
            {
                "title": item["title"],
                "category": item["category"],
                "source": item["source"],
            }
        )

    embeddings = model.encode(
        documents,
        show_progress_bar=True,
        convert_to_numpy=True,
    ).tolist()

    try:
        collection.delete(ids=ids)
    except Exception:
        pass

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"\nStored {len(ids)} documents in ChromaDB."
    )


def main() -> None:
    """
    Main ingestion workflow.
    """

    print("=" * 60)
    print("Semantic Refund Search - Data Ingestion")
    print("=" * 60)

    dataset = load_dataset()

    print(
        f"\nLoaded {len(dataset)} policy chunks."
    )

    print(
        f"\nLoading embedding model: {EMBEDDING_MODEL}"
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    collection = get_collection()

    ingest_documents(
        dataset,
        collection,
        model,
    )

    print("\nCollection:", COLLECTION_NAME)
    print("Database :", CHROMA_DB_DIR)
    print("\nDone.\n")


if __name__ == "__main__":
    main()