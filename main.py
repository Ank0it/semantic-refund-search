"""
Main entry point for the Semantic Refund Search API.
"""

from fastapi import FastAPI

from app.api import router

app = FastAPI(
    title="Semantic Refund Search API",
    description=(
        "Semantic search service for a Refund Policy knowledge base. "
        "This project retrieves the top 3 relevant policy chunks "
        "using vector similarity search. "
        "It does not generate final answers."
    ),
    version="1.0.0",
)

app.include_router(router)


@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "running",
        "service": "Semantic Refund Search API",
        "version": "1.0.0",
    }