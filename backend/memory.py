# backend/memory.py
import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver


def build_checkpoint_store(path: str = "./data/pci_memory.sqlite") -> SqliteSaver:
    """
    Return a SQLite-backed LangGraph checkpointer.

    Compatible with all langgraph versions (no create_if_missing keyword).
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    return SqliteSaver(conn)
