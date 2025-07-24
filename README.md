# PCI LangGraph Chatbot 🧩🔮  

A tiny, fully-local demo that stitches together **LangGraph**, **FastAPI**, **Streamlit**, and a **local LLM served by [Ollama](https://ollama.com)**.  
Ask any product-related question; the graph will (1) detect the customer segment, (2) call an LLM, then (3) show a three-line suggestion in the UI.

---

## ✨ Project Highlights
| Layer | Library | File | Purpose |
|-------|---------|------|---------|
| **Frontend** | Streamlit | `frontend/app.py` | Simple chat UI ↔ backend HTTP |
| **API** | FastAPI | `backend/main.py` | `/query` & `/health` endpoints |
| **State machine** | LangGraph | `backend/graph.py` | context → segment → suggestion |
| **LLM call** | Ollama Python | `backend/suggestion.py` | local inference (no cloud costs) |
| **Memory / checkpoints** | SQLite | `backend/memory.py` | conversation-level persistence |

---

## 🖥️ Quick Start (TL;DR)

```bash
git clone https://github.com/akhtarfarhan/pci_langgraph.git
cd pci_langgraph

# create & activate virtual-env
python -m venv .venv
.\.venv\Scripts\ctivate      # PowerShell / cmd
# source .venv/bin/activate   # Bash / zsh

pip install -r requirements.txt

# 1️⃣ make sure one Ollama daemon is running
ollama serve                    # leave it in its own terminal
ollama pull llama3:8b           # once, ~4 GB

# 2️⃣ backend API
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 3️⃣ frontend UI
streamlit run frontend/app.py
```

Open **http://localhost:8501** → chat away!

---

## 🗂️ Repo Structure

```
pci_langgraph/
│
├─ backend/
│  ├─ __init__.py
│  ├─ main.py          # FastAPI app
│  ├─ graph.py         # LangGraph pipeline
│  ├─ segmentation.py  # heuristic segment detector
│  ├─ suggestion.py    # Ollama prompt + call
│  └─ memory.py        # SQLite checkpoint helper
│
├─ frontend/
│  └─ app.py           # Streamlit chat UI
│
├─ data/               # created at runtime for SQLite DB
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## 🔌 Detailed Setup

### 1. Prerequisites
| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.9 – 3.12 | Tested on 3.11 |
| Git | any | for cloning / pushing |
| Ollama | 0.1.32 + | <https://ollama.com/download> |
| (Windows) VC++ Redistributable | latest | Ollama requirement |

> **GPU?** Not required—CPU runs fine; GPU (CUDA/Metal) speeds things up.

### 2. Clone & virtual-env

```bash
git clone https://github.com/akhtarfarhan/pci_langgraph.git
cd pci_langgraph
python -m venv .venv
.\.venv\Scriptsctivate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the LLM

```bash
ollama serve                 # one instance only
ollama pull llama3:8b        # change model in backend/suggestion.py if desired
```

### 5. Run the backend API

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
# -> http://localhost:8000/docs  (FastAPI Swagger UI)
```

### 6. Run the Streamlit frontend

```bash
streamlit run frontend/app.py
# -> http://localhost:8501
```

---

## 🛠️ Configuration

| Variable / file | Default | Meaning |
|-----------------|---------|---------|
| `MODEL_NAME` in `backend/suggestion.py` | `"llama3:8b"` | Any model you have locally (e.g. `llama2:13b`, `phi3:mini`) |
| `BACKEND` in `frontend/app.py` | `http://localhost:8000/query` | Change if you host the API elsewhere |
| `.venv/` | *ignored* | Python virtual-env |
| `data/pci_memory.sqlite` | runtime | Conversation checkpoints |

---

## 🔍 API Reference

### `GET /health`
Simple liveness probe.

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### `POST /query`
```json
Request body:
{
  "messages": [
    {"role": "user", "content": "I want a cheap phone"}
  ]
}
Headers:
session-id: demo
```

```json
Successful response:
{
  "segment": "Value-Seeker",
  "suggestion": "Looks like you’re after an affordable option …",
  "messages": [
    {"role": "user", "content": "I want a cheap phone"},
    {"role": "assistant", "content": "Looks like you’re after …"}
  ]
}
```

---

## 🚑 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Error: listen tcp 127.0.0.1:11434` | Another Ollama instance already running—use it or kill it. |
| `AttributeError: module 'ollama' has no attribute 'ollama'` | You’re on the new client API; ensure `backend/suggestion.py` matches *this* repo. |
| Backend crashes with `SqliteSaver` arg error | You overwrote `backend/memory.py`—use the version here or upgrade `langgraph`. |
| Streamlit shows `Backend error 422: missing "session-id"` | `headers={"session-id": …}` (hyphen) in `frontend/app.py`. |

---

## 🧹 .gitignore (excerpt)

```gitignore
__pycache__/
*.py[cod]
.venv/
.vscode/
data/
*.sqlite
.DS_Store
Thumbs.db
```

---

## 👩‍💻 Development Tips

* **Hot-reload**: backend runs with `--reload`; Streamlit reloads on save.
* **Branching**: `git checkout -b feature/<name>` → push → open PR.
* **Linting/formatting**: add `ruff`, `black`, or `isort` as you like.
* **Testing**: integrate `pytest`; mock Ollama calls via `responses`.

---

## 📜 License

MIT © 2025 Farhan Akhtar  
See [`LICENSE`](LICENSE) for details.

---

## 🙏 Credits

* [LangGraph](https://github.com/langchain-ai/langgraph) – stateful graphs for LLMs  
* [FastAPI](https://fastapi.tiangolo.com/) – blazing-fast web framework  
* [Streamlit](https://streamlit.io/) – the fastest way to build data apps  
* [Ollama](https://ollama.com) – run LLMs locally with one command  
* Initial integration and troubleshooting compiled with help from ChatGPT.
* 

#PROJECT REPORT
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
        D[Checkpoint Store\n(SQLite or Memory)]
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

| File | Responsibility                                                     |
| ---- | ------------------------------------------------------------------ |
| ``   | Streamlit chat UI, talks to backend via `requests`                 |
| ``   | FastAPI app (`/health`, `/query`)                                  |
| ``   | Defines `StateGraph` with three nodes                              |
| ``   | Heuristic customer‑segment classifier                              |
| ``   | Builds prompt & calls Ollama ‑> returns suggestion                 |
| ``   | Provides best‑available checkpointer (SQLite ⚙️→ Memory 🧠→ No‑op) |
| ``   | Pin runtime dependencies                                           |
| ``   | Excludes venv, data, logs, build artefacts                         |

---

## 4  Setup & Execution

```bash
# clone & enter
git clone https://github.com/akhtarfarhan/pci_langgraph.git
cd pci_langgraph

# venv
python -m venv .venv
.\.venv\Scripts\activate   # (or source .venv/bin/activate)

# deps
pip install -r requirements.txt

# one‑time model pull
ollama serve        # separate terminal
ullama pull llama3:8b

# backend
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload

# frontend (new terminal)
streamlit run frontend/app.py
```

Open [**http://localhost:8501**](http://localhost:8501) and chat away.

---

## 5  Key Design Decisions

1. **Local‑first**: All inference runs on‑device via Ollama → no API keys, works offline.
2. **Resilient checkpointing**: `memory.py` falls back gracefully if SQLite extras are missing.
3. **Stateless API, stateful graph**: FastAPI handles each request statelessly; LangGraph manages per‑session memory via checkpoint store.
4. **Hot‑reload everywhere**: Uvicorn’s `--reload` + Streamlit’s auto‑refresh speeds up dev loop.

---

## 6  Reflections & Challenges

| Challenge                                                  | Solution / Lesson                                                                      |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Dependency drift in LangGraph (`SqliteSaver` path changes) | Added multi‑path import + memory fallback to keep code future‑proof.                   |
| Windows file‑lock on `.venv` DLLs during Git rebase        | `.gitignore` excludes `.venv/`; rebasing issues vanished.                              |
| Conflicting Python interpreters (Anaconda vs venv)         | Always launch with venv’s explicit `python.exe`.                                       |
| Streamlit 422 error (missing `session‑id` header)          | Changed header name to hyphen version to satisfy FastAPI’s underscore‑conversion rule. |

Overall, the project demonstrates how small, focused Python modules can be composed into a full local‑LLM product demo with minimal lines of code.

---

## 7  Future Work

- **Persistent user profiles** (e.g. Redis backend instead of SQLite).
- **Rich UI**: product carousels, images, and ratings via Streamlit components.
- **Better segmentation**: train a small ML model or use embedding similarity.
- **Docker container** for push‑button deployment.

---

## 8  Demo Checklist

-

---

> **Author:** Farhan Akhtar — July 2025


