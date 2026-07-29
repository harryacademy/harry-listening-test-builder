"""Save/load Script objects as JSON files."""

import json
import re
from pathlib import Path

from scripts.models import Script

_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_\-]+")


def sanitize_filename(name: str) -> str:
    cleaned = _SAFE_NAME_RE.sub("_", name.strip())
    return cleaned or "untitled"


def save_script(script: Script, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{sanitize_filename(script.name)}.json"
    path.write_text(json.dumps(script.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_script(path: Path) -> Script:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Script.from_dict(data)


def list_saved_scripts(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))
