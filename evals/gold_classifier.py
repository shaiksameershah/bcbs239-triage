import json

import numpy as np
import ollama
from sklearn.linear_model import LogisticRegression

from evals.metrics import report

train = json.load(open("data/splits/train.json"))
Xtr = np.load("data/cache/train_X.npy").astype("float64")
gold = json.load(open("data/gold.json"))
E = np.array(
    ollama.embed(model="nomic-embed-text", input=[g["text"] for g in gold])["embeddings"],
    dtype="float64",
)
E /= np.linalg.norm(E, axis=1, keepdims=True)

pred = {}
for field in ("principle", "severity"):
    clf = LogisticRegression(max_iter=3000, class_weight="balanced").fit(Xtr, [r[field] for r in train])
    pred[field] = list(clf.predict(E))

report(
    [g["principle"] for g in gold],
    [g["severity"] for g in gold],
    pred["principle"],
    pred["severity"],
    label="embedding + logistic regression",
)
