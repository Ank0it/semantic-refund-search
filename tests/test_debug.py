from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_debug_endpoint():
    response = client.get(
        "/debug/search",
        params={
            "query": "damaged product"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "query" in body
    assert "retrieved_chunks" in body

    assert len(body["retrieved_chunks"]) <= 3


def test_debug_contains_metadata():
    response = client.get(
        "/debug/search",
        params={
            "query": "refund"
        },
    )

    chunks = response.json()["retrieved_chunks"]

    for chunk in chunks:

        assert "score" in chunk
        assert "text" in chunk
        assert "metadata" in chunk