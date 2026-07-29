"""Factory for looking up TTS providers by name.

The UI and other callers should get providers through here rather than
importing a specific provider module directly, so adding a new backend
(e.g. "google-tts") is a one-line addition to _PROVIDERS.
"""

from tts.base import TTSProvider
from tts.edge_provider import EdgeTTSProvider

_PROVIDERS: dict[str, TTSProvider] = {}


def get_provider(name: str = "edge-tts") -> TTSProvider:
    if name not in _PROVIDERS:
        if name == "edge-tts":
            _PROVIDERS[name] = EdgeTTSProvider()
        else:
            raise ValueError(f"Unknown TTS provider: {name}")
    return _PROVIDERS[name]


def available_providers() -> list[str]:
    return ["edge-tts"]
