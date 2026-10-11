import json
import pathlib

LOG = pathlib.Path("data/log.json")


def load() -> list[dict]:
    return json.loads(LOG.read_text()) if LOG.exists() else []


def save(entries: list[dict]) -> None:
    LOG.write_text(json.dumps(entries))