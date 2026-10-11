import numpy as np
import ollama

from .schema import Triage

CHAT_MODEL = "llama3.1:8b"
EMBED_MODEL = "nomic-embed-text"


def embed(text: str) -> list[float]:
    return ollama.embed(model=EMBED_MODEL, input=text)["embeddings"][0]


def cosine(a, b) -> float:
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def classify(system: str, user: str, retries: int = 2) -> Triage:
    last_error = None
    for _ in range(retries + 1):
        try:
            resp = ollama.chat(
                model=CHAT_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                format=Triage.model_json_schema(),
                options={"temperature": 0},
            )
            return Triage.model_validate_json(resp["message"]["content"])
        except Exception as e:
            last_error = e
    raise last_error