# PCI LangGraph Chatbot — Project Report

---

## 1  Overview

**PCI LangGraph Chatbot** is a fully‑local proof‑of‑concept that stitches together four modern Python stacks:

| Layer         | Library                   | Role                                                          |
| ------------- | ------------------------- | ------------------------------------------------------------- |
| UI            | **Streamlit**             | Chat interface in the browser                                 |
| API           | **FastAPI** + **Uvicorn** | REST endpoint (`/query`) that LangGraph invokes               |
| State Machine | **LangGraph**             | 3‑step graph → ① context ② segment detection ③ LLM suggestion |
| LLM Runtime   | **Ollama**                | Local LLM (default: `llama3:8b`) for zero cloud cost          |

The application detects a user’s customer segment (Value‑Seeker, Premium, Tech‑Enthusiast, General), calls a local LLM to craft a short product suggestion, and streams the result back to the UI.

---

## 2  Architecture Diagram

```mermaid
flowchart LR
    subgraph Frontend
        A[Streamlit UI]
    end
    subgraph Backend
        B(FastAPI / Uvicorn)
        C[LangGraph Graph\ncontext → segment → suggest]
        D[Checkpoint Store\n(SQLite / Memory / No‑op)]
        E[Ollama Daemon\n(local LLM)]
    end

    A -- HTTP → B
    B -- invoke --> C
    C -- load/dump --> D
    C -- prompt ➜ E
    E -- response --> C
    C -- JSON --> B
    B -- JSON --> A
```

---

## 3  Module Breakdown

| File | Responsibility                                      |
| ---- | --------------------------------------------------- |
| ``   | Streamlit chat UI, calls backend via `requests`     |
| ``   | FastAPI app exposing `/health` & `/query`           |
| ``   | Declares LangGraph state‑machine (3 nodes)          |
| ``   | Heuristic customer‑segment classifier               |
| ``   | Builds prompt and queries Ollama for suggestion     |
| ``   | Adaptive checkpoint store (SQLite → Memory → No‑op) |
| ``   | Pins runtime dependencies                           |
| ``   | Excludes venv, data, build artefacts                |

All modules are **well‑commented** and follow single‑responsibility principles, making the codebase easy to extend and maintain.

---

## 4  Setup & Execution

```bash
# clone & enter
git clone https://github.com/akhtarfarhan/pci_langgraph.git
cd pci_langgraph

# virtual‑env
python -m venv .venv
.\.venv\Scripts\activate     # (or: source .venv/bin/activate)

# dependencies
pip install -r requirements.txt

# one‑time model pull (separate terminal)
ollama serve                   # starts daemon
ollama pull llama3:8b

# backend
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload

# frontend (new terminal)
streamlit run frontend/app.py
```

Open [**http://localhost:8501**](http://localhost:8501) and start chatting.

---

## 5  Key Design Decisions

1. **Local‑first**: All inference runs on‑device via Ollama → no API keys, works offline.
2. **Resilient checkpointing**: `memory.py` gracefully falls back if SQLite extras are missing.
3. **Stateless API, stateful graph**: FastAPI handles each request statelessly; LangGraph manages per‑session memory via the checkpoint store.
4. **Hot‑reload everywhere**: Uvicorn’s `--reload` and Streamlit’s auto‑refresh speed up development.
5. **Modular code**: Each concern lives in its own file; functions are type‑annotated and documented.

---

## 6  Reflections & Challenges

| Challenge                                                  | Solution / Lesson                                                 |
| ---------------------------------------------------------- | ----------------------------------------------------------------- |
| Dependency drift in LangGraph (`SqliteSaver` path changes) | Added multi‑path import plus an in‑memory fallback.               |
| Windows file‑lock on `.venv` DLLs during Git operations    | `.gitignore` excludes `.venv/`; resolved rebase issues.           |
| Conflicting Python interpreters (Anaconda vs venv)         | Always launch tools with the venv’s explicit `python.exe`.        |
| FastAPI 422 error (missing `session‑id` header)            | Renamed header to hyphenated form to match FastAPI parsing rules. |

Overall, small, focused Python modules compose into a full local‑LLM product demo with minimal code.

---

## 7  Future Work

- **Persistent user profiles** (e.g. Redis instead of SQLite).
- **Rich UI**: product carousels, image previews, & rating badges.
- **Smarter segmentation**: embed queries & run k‑NN over past users.
- **Docker container** for one‑command deployment.

> **Author:** Farhan Akhtar — July 2025

