# frontend/app.py
import streamlit as st
import requests
from typing import List, Dict

BACKEND = "http://localhost:8000/query"
SESSION_ID = "demo"          # any string keeps history per user

st.title("🔮 PCI Chat")

# ─── conversation memory ────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history: List[Dict] = []

# ─── render previous turns ──────────────────────────────────────────────
for m in st.session_state.history:
    st.chat_message(m["role"]).write(m["content"])

# ─── input box ──────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything…"):
    # show user message immediately
    st.chat_message("user").write(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # ▸▸▸ call the FastAPI backend
    response = requests.post(
        BACKEND,
        headers={"session-id": SESSION_ID},   # ← hyphen, matches backend
        json={"messages": st.session_state.history},
        timeout=120,
    )

    # graceful error-handling
    if response.status_code != 200:
        st.error(f"Backend error {response.status_code}: {response.text}")
        st.stop()

    data = response.json()
    if not {"messages", "suggestion"}.issubset(data):
        st.error(f"Unexpected response format:\n{data}")
        st.stop()

    # update chat history & display assistant reply
    st.session_state.history = data["messages"]
    st.chat_message("assistant").write(data["suggestion"])
