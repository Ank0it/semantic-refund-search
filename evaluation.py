"""
Evaluate semantic retrieval quality.

Checks whether the expected category appears in the
Top 3 retrieved chunks for each evaluation query.
"""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

QUERY_FILE = Path("tests") / "evaluation_queries.json"


def load_queries():
    with open(QUERY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate():
    queries = load_queries()

    total = 0
    correct = 0

    print("=" * 80)
    print("Semantic Retrieval Evaluation")
    print("=" * 80)

    for item in queries:

        total += 1

        query = item["query"]
        expected = item["expected_category"]

        response = client.post(
            "/search",
            json={"query": query},
        )

        response.raise_for_status()

        results = response.json()["results"]

        retrieved_categories = [
            r["metadata"]["category"]
            for r in results
        ]

        if expected is None:
            success = len(results) == 0
        else:
            success = expected in retrieved_categories

        if success:
            correct += 1

        status = "PASS" if success else "FAIL"

        print(
            f"[{status}] {query}\n"
            f"Expected : {expected}\n"
            f"Retrieved: {retrieved_categories}\n"
        )

    accuracy = (correct / total) * 100

    print("=" * 80)
    print(f"Correct   : {correct}/{total}")
    print(f"Accuracy  : {accuracy:.2f}%")

    if correct >= 15:
        print("Assignment Target: PASSED (>=15/20)")
    else:
        print("Assignment Target: FAILED (<15/20)")
    print("=" * 80)


if __name__ == "__main__":
    evaluate()