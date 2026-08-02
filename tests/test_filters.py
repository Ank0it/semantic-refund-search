from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_filter_returns_status_200():
    response = client.post(
        "/search/filter",
        json={
            "query": "refund",
            "category": "Refund"
        },
    )

    assert response.status_code == 200


def test_filter_contains_only_requested_category():
    response = client.post(
        "/search/filter",
        json={
            "query": "refund",
            "category": "Refund"
        },
    )

    data = response.json()["results"]

    for result in data:
        assert (
            result["metadata"]["category"]
            == "Refund"
        )


def test_filter_returns_max_three():
    response = client.post(
        "/search/filter",
        json={
            "query": "refund",
            "category": "Refund"
        },
    )

    assert len(response.json()["results"]) <= 3