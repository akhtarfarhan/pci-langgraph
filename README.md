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
