# Semantic Refund Search

A production-style semantic search service built with **FastAPI**, **ChromaDB**, and **Sentence Transformers**. The system indexes a structured Refund Policy knowledge base and retrieves the **Top 3 most relevant policy chunks** using vector similarity search.

This project focuses purely on the **retrieval layer** of a Retrieval-Augmented Generation (RAG) pipeline. It intentionally does **not** generate final answers with an LLM, allowing retrieval quality to be evaluated independently.

---

## Project Objectives

* Build a semantic search API over a real business knowledge base.
* Store 50–100 document chunks in a vector database.
* Return the Top 3 most relevant chunks.
* Include similarity scores and source metadata.
* Support metadata-based filtering.
* Provide a retrieval debugging endpoint.
* Evaluate retrieval quality using unseen queries.
* Analyze retrieval failures and suggest improvements.

---

## Features

* Semantic search using Sentence Transformers
* ChromaDB vector database
* FastAPI REST API
* Metadata filtering
* Debug retrieval endpoint
* Retrieval evaluation script
* Automated test suite
* Modular project architecture

---

## Tech Stack

| Component        | Technology            |
| ---------------- | --------------------- |
| Language         | Python 3.11           |
| API Framework    | FastAPI               |
| Vector Database  | ChromaDB              |
| Embedding Model  | all-MiniLM-L6-v2      |
| Machine Learning | Sentence Transformers |
| Testing          | Pytest                |
| Server           | Uvicorn               |

---

# Project Structure

```text
semantic-refund-search/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── ingest.py
│   ├── models.py
│   └── search.py
│
├── data/
│   └── refund_policy.json
│
├── docs/
│   └── retrieval_analysis.md
│
├── tests/
│   ├── evaluation_queries.json
│   ├── test_debug.py
│   ├── test_filters.py
│   └── test_search.py
│
├── chroma_db/
│
├── evaluation.py
├── main.py
├── requirements.txt
└── README.md
```

---

# System Architecture

```text
                    Refund Policy Dataset
                             │
                             ▼
                     Data Ingestion Script
                             │
                             ▼
                  Sentence Transformer Model
                    (all-MiniLM-L6-v2)
                             │
                             ▼
                         ChromaDB
                             │
          ┌──────────────────┴──────────────────┐
          ▼                                     ▼
      /search                          /search/filter
          │                                     │
          └──────────────┬──────────────────────┘
                         ▼
               Top 3 Relevant Chunks
                         │
                         ▼
            Similarity Score + Metadata

                   /debug/search
                         │
                         ▼
              Retrieval Inspection
```

---

# Knowledge Base

Domain:

> **Refund Policy Knowledge Base**

The knowledge base contains **70 policy chunks** covering business rules such as:

* Returns
* Refunds
* Exchanges
* Orders
* Payments
* Warranty
* Customer Support

Each document contains:

* Policy ID
* Title
* Category
* Source
* Policy Content

---

# Chunking Strategy

Each refund policy section is stored as an independent semantic chunk.

Each chunk contains:

* One complete policy statement
* Category metadata
* Source metadata
* Title metadata

This strategy preserves semantic meaning while keeping retrieval granular and easy to debug.

### Advantages

* Better semantic understanding
* Precise retrieval
* Rich metadata
* Easier debugging
* Independent document indexing

### Trade-offs

* Small chunks may lose surrounding context.
* Larger chunks reduce retrieval precision.
* Missing synonyms can negatively impact recall.

---

# Data Ingestion

Generate embeddings and populate ChromaDB.

```bash
python app/ingest.py
```

This script:

* Loads the refund policy dataset
* Generates embeddings
* Creates the ChromaDB collection
* Stores all policy chunks

---

# Running the API

```bash
uvicorn main:app --reload
```

API available at

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Search

```
POST /search
```

Example Request

```json
{
    "query": "Can I return a damaged product?"
}
```

Example Response

```json
{
    "results": [
        {
            "score": 0.59,
            "text": "...",
            "metadata": {
                "category": "Returns",
                "title": "Damaged Products",
                "source": "Refund Policy"
            }
        }
    ]
}
```

---

## Metadata Filter Search

```
POST /search/filter
```

Example

```json
{
    "query": "refund delay",
    "category": "Payments"
}
```

---

## Debug Endpoint

```
GET /debug/search
```

Example

```
/debug/search?query=damaged product
```

Returns the retrieved chunks with similarity scores and metadata for inspection and debugging.

---

# Evaluation

The retrieval system is evaluated using **20 unseen queries**.

Run:

```bash
python evaluation.py
```

Current Results

| Metric                 |      Value |
| ---------------------- | ---------: |
| Total Queries          |         20 |
| Correct Retrievals     |         16 |
| Accuracy               |    **80%** |
| Assignment Requirement | **Passed** |

The system successfully retrieves the expected policy category within the Top 3 results for **16 out of 20 unseen evaluation queries**.

---

# Retrieval Analysis

Four queries were not retrieved correctly.

| Query                      | Expected | Root Cause                  | Planned Improvement                                              |
| -------------------------- | -------- | --------------------------- | ---------------------------------------------------------------- |
| Wrong item                 | Returns  | Missing synonyms            | Add "wrong item", "incorrect item", "received different product" |
| Refund hasn't reached bank | Payments | Limited payment vocabulary  | Expand payment terminology                                       |
| Undo purchase              | Orders   | Missing alternative wording | Add "undo purchase", "reverse order", "cancel purchase"          |
| Warranty                   | Warranty | Limited warranty content    | Expand warranty-specific policy chunks                           |

Most failures are caused by **dataset vocabulary limitations**, not by the retrieval engine itself.

---

# Testing

Run the complete test suite

```bash
pytest -v
```

Current Status

```
9 passed
```

---

# Evaluation Script

The evaluation script measures retrieval quality against unseen queries.

```bash
python evaluation.py
```

Metrics reported:

* Correct retrievals
* Accuracy
* Pass rate
* Assignment target status

---

# Similarity Scores

Each retrieved chunk includes:

* Semantic similarity score
* Category metadata
* Title metadata
* Source metadata

This makes retrieval transparent and easy to inspect.

---

# Future Improvements

Potential enhancements include:

* Retrieval-Augmented Generation (RAG)
* Hybrid Search (Keyword + Vector Search)
* Cross-Encoder Re-ranking
* Dynamic similarity threshold
* Synonym expansion
* Query rewriting
* Multi-vector retrieval
* LLM-powered grounded answer generation

---

# Installation

Clone the repository

```bash
git clone https://github.com/Ank0it/semantic-refund-search.git
```

Move into the project

```bash
cd semantic-refund-search
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Populate the vector database

```bash
python app/ingest.py
```

Start the API

```bash
uvicorn main:app --reload
```

---

# Assignment Requirements Checklist

* ✅ Real business knowledge base
* ✅ 70 document chunks
* ✅ ChromaDB vector database
* ✅ Semantic retrieval API
* ✅ Top 3 retrieval
* ✅ Similarity scores
* ✅ Metadata in results
* ✅ Metadata filtering
* ✅ Debug endpoint
* ✅ Retrieval evaluation script
* ✅ Retrieval quality ≥ 15/20 (16/20 achieved)
* ✅ Retrieval analysis
* ✅ Chunking strategy explanation
* ✅ Automated tests

---

# License

This project is intended for educational purposes as part of an AI Engineering semantic search assignment.
