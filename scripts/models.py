"""Data model for a test script: an ordered list of speech lines and pauses."""

from dataclasses import dataclass, field
from uuid import uuid4


def _new_id() -> str:
    return uuid4().hex[:8]


@dataclass
class ScriptLine:
    """One row in the script builder.

    kind == "speech": role, voice_id, and text are used.
    kind == "pause": only pause_ms is used (a standalone silence gap).
    """

    kind: str = "speech"  # "speech" | "pause"
    id: str = field(default_factory=_new_id)
    role: str = ""
    voice_id: str = ""
    text: str = ""
    pause_ms: int = 500

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "id": self.id,
            "role": self.role,
            "voice_id": self.voice_id,
            "text": self.text,
            "pause_ms": self.pause_ms,
        }

    @staticmethod
    def from_dict(data: dict) -> "ScriptLine":
        return ScriptLine(
            kind=data.get("kind", "speech"),
            id=data.get("id", _new_id()),
            role=data.get("role", ""),
            voice_id=data.get("voice_id", ""),
            text=data.get("text", ""),
            pause_ms=data.get("pause_ms", 500),
        )


@dataclass
class Script:
    """A full test script: metadata plus an ordered list of lines."""

    name: str = "untitled"
    mode: str = "multi"  # "single" | "multi"
    filename_pattern: str = "{testname}_{date}.mp3"
    lines: list[ScriptLine] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "mode": self.mode,
            "filename_pattern": self.filename_pattern,
            "lines": [line.to_dict() for line in self.lines],
        }

    @staticmethod
    def from_dict(data: dict) -> "Script":
        return Script(
            name=data.get("name", "untitled"),
            mode=data.get("mode", "multi"),
            filename_pattern=data.get("filename_pattern", "{testname}_{date}.mp3"),
            lines=[ScriptLine.from_dict(line) for line in data.get("lines", [])],
        )
