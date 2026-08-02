"""
Tests for the /search endpoint.
"""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


QUERY_FILE = (
    Path(__file__).parent / "evaluation_queries.json"
)


def load_queries():
    """Load evaluation queries."""

    with open(QUERY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def test_search_returns_status_200():
    """
    Verify the endpoint is reachable.
    """

    response = client.post(
        "/search",
        json={
            "query": "Can I return a damaged product?"
        },
    )

    assert response.status_code == 200


def test_search_returns_top_three():
    """
    Verify exactly Top 3 chunks are returned.
    """

    response = client.post(
        "/search",
        json={
            "query": "Refund after 15 days"
        },
    )

    data = response.json()

    assert "results" in data

    assert len(data["results"]) == 3


def test_every_result_has_required_fields():
    """
    Every search result should contain the required fields.
    """

    response = client.post(
        "/search",
        json={
            "query": "Refund"
        },
    )

    results = response.json()["results"]

    for item in results:

        assert "score" in item

        assert "text" in item

        assert "metadata" in item

        metadata = item["metadata"]

        assert "title" in metadata

        assert "category" in metadata

        assert "source" in metadata


def test_all_evaluation_queries_execute():
    """
    Ensure every evaluation query returns
    a valid response.
    """

    queries = load_queries()

    for query in queries:

        response = client.post(
            "/search",
            json={
                "query": query["query"]
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert "results" in body

        assert len(body["results"]) <= 3