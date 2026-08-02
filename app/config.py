"""
Application configuration.

This module contains all configurable constants used across the project.
Keeping them in one place makes the project easier to maintain.
"""

from pathlib import Path

# -----------------------------
# Base Directories
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# -----------------------------
# Dataset
# -----------------------------

DATASET_PATH = DATA_DIR / "refund_policy.json"

# -----------------------------
# ChromaDB
# -----------------------------

COLLECTION_NAME = "refund_policy"

# -----------------------------
# Embedding Model
# -----------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# -----------------------------
# Retrieval
# -----------------------------

TOP_K = 3