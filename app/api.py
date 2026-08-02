"""
FastAPI routes for the Semantic Refund Search project.

Endpoints:
- POST /search
- POST /search/filter
- GET /debug/search
"""

from fastapi import APIRouter, HTTPException

from app.models import (
    FilterSearchRequest,
    Metadata,
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.search import search_engine

router = APIRouter()


@router.post(
    "/search",
    response_model=SearchResponse,
    tags=["Semantic Search"],
)
def semantic_search(request: SearchRequest):
    """
    Perform semantic search and return the top matching chunks.
    """

    try:
        results = search_engine.search(request.query)

        response = SearchResponse(
            results=[
                SearchResult(
                    score=result["score"],
                    text=result["text"],
                    metadata=Metadata(**result["metadata"]),
                )
                for result in results
            ]
        )

        return response

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post(
    "/search/filter",
    response_model=SearchResponse,
    tags=["Semantic Search"],
)
def filtered_semantic_search(request: FilterSearchRequest):
    """
    Perform semantic search with metadata filtering.
    """

    try:
        results = search_engine.filtered_search(
            query=request.query,
            category=request.category,
            title=request.title,
            source=request.source,
        )

        response = SearchResponse(
            results=[
                SearchResult(
                    score=result["score"],
                    text=result["text"],
                    metadata=Metadata(**result["metadata"]),
                )
                for result in results
            ]
        )

        return response

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/debug/search",
    tags=["Debug"],
)
def debug_search(query: str):
    """
    Debug endpoint.

    Returns the raw retrieved chunks with similarity scores
    and metadata exactly as produced by the search engine.
    """

    try:
        return {
            "query": query,
            "retrieved_chunks": search_engine.search(query),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )