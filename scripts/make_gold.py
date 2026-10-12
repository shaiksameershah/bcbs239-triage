import csv
import json
import random

test = json.load(open("data/splits/test.json"))
random.seed(7)
crit = [r for r in test if r["severity"] == "critical"]
rest = [r for r in test if r["severity"] != "critical"]
pick = random.sample(crit, min(40, len(crit))) + random.sample(rest, min(80, len(rest)))
random.shuffle(pick)
with open("data/gold_review.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "text", "my_principle", "my_severity"])
    for i, r in enumerate(pick):
        w.writerow([i, r["text"], "", ""])
json.dump(pick, open("data/gold_key.json", "w"))
print(len(pick), "rows written to data/gold_review.csv")
