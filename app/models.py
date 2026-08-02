"""
Pydantic models used by the Semantic Refund Search API.

These models define the request and response schema for the API endpoints.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """
    Request body for semantic search.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="User search query."
    )


class FilterSearchRequest(BaseModel):
    """
    Request body for metadata filtered search.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="User search query."
    )

    category: Optional[str] = Field(
        default=None,
        description="Category metadata filter."
    )

    title: Optional[str] = Field(
        default=None,
        description="Title metadata filter."
    )

    source: Optional[str] = Field(
        default=None,
        description="Source metadata filter."
    )


class Metadata(BaseModel):
    """
    Metadata associated with each retrieved chunk.
    """

    title: str
    category: str
    source: str


class SearchResult(BaseModel):
    """
    A single semantic search result.
    """

    score: float = Field(
        ...,
        description="Similarity score."
    )

    text: str

    metadata: Metadata


class SearchResponse(BaseModel):
    """
    Response returned by /search and /search/filter.
    """

    results: List[SearchResult]