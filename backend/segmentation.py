from typing import Literal

Segment = Literal["Value-Seeker", "Premium", "Tech-Enthusiast", "General"]

def segment_customer(query: str) -> Segment:
    q = query.lower()
    if any(k in q for k in ("discount", "cheap", "price")):
        return "Value-Seeker"
    if "latest" in q or "flagship" in q:
        return "Tech-Enthusiast"
    if any(k in q for k in ("luxury", "premium", "exclusive")):
        return "Premium"
    return "General"
