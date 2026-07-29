"""edge-tts backed implementation of TTSProvider."""

import asyncio

import edge_tts

from tts.base import TTSProvider, Voice

# edge-tts locale region -> display accent label. Regions not listed here
# fall back to using the region code itself (e.g. "CA", "SG").
_ACCENT_OVERRIDES = {
    "GB": "UK",
}

_LANGUAGE_NAMES = {
    "en": "English",
    "vi": "Vietnamese",
}

# Only these languages are surfaced in the UI for now.
_SUPPORTED_LANG_PREFIXES = tuple(_LANGUAGE_NAMES.keys())


def _voice_to_model(raw: dict) -> Voice | None:
    locale = raw["Locale"]  # e.g. "en-US", "vi-VN"
    lang_prefix, _, region = locale.partition("-")
    if lang_prefix not in _SUPPORTED_LANG_PREFIXES:
        return None

    language = _LANGUAGE_NAMES[lang_prefix]
    accent = "Standard" if language == "Vietnamese" else _ACCENT_OVERRIDES.get(region, region)
    short_name = raw["ShortName"]  # e.g. "en-US-AriaNeural"
    friendly = short_name.split("-")[-1].replace("Neural", "").replace("Multilingual", " (Multilingual)")

    return Voice(
        id=short_name,
        display_name=f"{friendly} — {language} ({accent}, {raw['Gender']})",
        language=language,
        locale=locale,
        gender=raw["Gender"],
        accent=accent,
        provider="edge-tts",
    )


class EdgeTTSProvider(TTSProvider):
    def __init__(self):
        self._voices_cache: list[Voice] | None = None

    def list_voices(self) -> list[Voice]:
        if self._voices_cache is None:
            raw_voices = asyncio.run(edge_tts.list_voices())
            voices = (_voice_to_model(v) for v in raw_voices)
            self._voices_cache = sorted(
                (v for v in voices if v is not None),
                key=lambda v: (v.language, v.accent, v.display_name),
            )
        return self._voices_cache

    def synthesize(self, text: str, voice_id: str, output_path: str) -> None:
        async def _run():
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(output_path)

        asyncio.run(_run())
