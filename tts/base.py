"""Provider-agnostic TTS abstraction.

Any new backend (Google Cloud TTS, etc.) implements TTSProvider and returns
Voice objects in this shape. The UI only ever depends on this file.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Voice:
    """Normalized voice metadata, independent of provider-specific formats."""

    id: str  # provider-specific identifier passed back into synthesize()
    display_name: str  # human-friendly label for the UI
    language: str  # "English" or "Vietnamese"
    locale: str  # e.g. "en-US", "vi-VN"
    gender: str  # "Male" or "Female"
    accent: str  # e.g. "US", "UK", "AU", "IN", "Standard" (VI has no variety)
    provider: str  # e.g. "edge-tts"


class TTSProvider(ABC):
    """Interface every TTS backend must implement."""

    @abstractmethod
    def list_voices(self) -> list[Voice]:
        """Return all voices this provider offers, in normalized form."""
        raise NotImplementedError

    @abstractmethod
    def synthesize(self, text: str, voice_id: str, output_path: str) -> None:
        """Render `text` with `voice_id` and write an mp3 file to `output_path`."""
        raise NotImplementedError
