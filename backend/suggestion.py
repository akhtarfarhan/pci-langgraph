# backend/suggestion.py
"""
Generate a short product suggestion with Ollama.
Requires the Ollama daemon running (http://localhost:11434 by default).
"""

import ollama

MODEL_NAME = "llama3:8b"       # pull once: `ollama pull llama3:8b`


def build_prompt(segment: str, query: str) -> str:
    return (
        "You are a product assistant.\n"
        f"Customer segment: {segment}\n"
        f"Customer query: {query}\n\n"
        "Answer in max 3 sentences:\n"
        "  • recognise the need\n"
        "  • suggest one product or offer tailored to the segment\n"
        "  • finish with a next step\n"
    )


def generate_suggestion(segment: str, query: str) -> str:
    prompt = build_prompt(segment, query)

    # call Ollama via chat()
    resp = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp["message"]["content"].strip()
