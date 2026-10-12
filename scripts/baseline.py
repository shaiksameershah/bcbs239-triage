import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


def load(name):
    return json.load(open(f"data/splits/{name}.json")), np.load(f"data/cache/{name}_X.npy")


train, Xtr = load("train")
dev, Xdv = load("dev")
for field in ("principle", "severity"):
    clf = LogisticRegression(max_iter=3000, class_weight="balanced").fit(Xtr, [r[field] for r in train])
    pred = clf.predict(Xdv)
    true = [r[field] for r in dev]
    print(f"\n=== {field} (dev set) ===")
    print(classification_report(true, pred, digits=3))
    labels = sorted(set(true))
    print(labels)
    print(confusion_matrix(true, pred, labels=labels))
