import json

ALLOWED_P = {
    "P2_architecture_lineage",
    "P3_accuracy_integrity",
    "P4_completeness",
    "P5_timeliness",
    "P6_adaptability",
}
ALLOWED_S = {"low", "medium", "high", "critical"}


def load_file(path):
    txt = open(path).read().strip()
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        data = [json.loads(line) for line in txt.splitlines() if line.strip()]
    if isinstance(data, dict):
        data = next((v for v in data.values() if isinstance(v, list)), [data])
    return data
