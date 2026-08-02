"""
Semantic search engine for the Refund Policy knowledge base.

Responsibilities:
- Load embedding model
- Connect to ChromaDB
- Perform semantic search
- Support metadata filtering
"""

from __future__ import annotations

from typing import Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from app.config import (
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)


class SemanticSearch:
    """
    Handles semantic retrieval from ChromaDB.
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR),
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_collection(
            COLLECTION_NAME
        )

    def search(
        self,
        query: str,
        top_k: int = TOP_K,
    ) -> list[dict]:
        """
        Perform semantic search.
        """

        embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return self._format_results(results)

    def filtered_search(
        self,
        query: str,
        category: Optional[str] = None,
        title: Optional[str] = None,
        source: Optional[str] = None,
        top_k: int = TOP_K,
    ) -> list[dict]:
        """
        Semantic search with metadata filtering.
        """

        embedding = self.model.encode(query).tolist()

        metadata_filter = {}

        if category:
            metadata_filter["category"] = category

        if title:
            metadata_filter["title"] = title

        if source:
            metadata_filter["source"] = source

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=metadata_filter if metadata_filter else None,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return self._format_results(results)

    @staticmethod
    def _format_results(results: dict) -> list[dict]:
        """
        Convert ChromaDB output into API-friendly format.
        """

        formatted = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            similarity = round(1 - float(distance), 4)

            formatted.append(
                {
                    "score": similarity,
                    "text": document,
                    "metadata": metadata,
                }
            )

        return formatted


search_engine = SemanticSearch()