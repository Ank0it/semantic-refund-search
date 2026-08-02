# Semantic Refund Search

A semantic search service built using FastAPI, Sentence Transformers, and ChromaDB.

## Objective

Retrieve the **Top 3 most relevant refund policy chunks** using semantic similarity.

This project intentionally **does not generate final answers**. It focuses only on retrieval.

---

## Tech Stack

- Python 3.11
- FastAPI
- ChromaDB
- Sentence Transformers
- all-MiniLM-L6-v2
- Pytest

---

## Project Structure

```text
app/
data/
tests/
main.py
requirements.txt
README.md
```

---

## Installation

```bash
python -m venv .venv

pip install -r requirements.txt
```

---

## Build Vector Database

```bash
python app/ingest.py
```

---

## Run API

```bash
uvicorn main:app --reload
```

---

## Swagger

```
http://127.0.0.1:8000/docs
```

---

## Endpoints

### POST /search

Returns:

- Top 3 chunks
- Similarity score
- Metadata

---

### POST /search/filter

Supports metadata filtering.

---

### GET /debug/search

Returns raw retrieved chunks for debugging.

---

## Running Tests

```bash
pytest -v
```

---

## Evaluation

The project includes:

- Semantic retrieval
- Metadata filtering
- Debug endpoint
- Similarity scores
- 20 evaluation queries
- Pytest suite

---

## Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Cross Encoder Re-ranking
- Answer generation using an LLM
- Retrieval evaluation metrics (Recall@3, MRR)