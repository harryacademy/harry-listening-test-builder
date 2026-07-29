"""Concatenate rendered speech clips and silence gaps into a single mp3."""

import os
import shutil
from pathlib import Path

from pydub import AudioSegment


def _find_ffmpeg_bin_dir() -> str | None:
    """Fall back to well-known Windows install locations if ffmpeg isn't
    yet on PATH for this process (e.g. installed via winget in a session
    that started before the PATH change propagated)."""
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return None  # already resolvable, nothing to do
    for pattern_root in (
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages",
        Path("C:/ProgramData/chocolatey/bin"),
    ):
        if pattern_root.exists():
            for candidate in pattern_root.glob("**/ffmpeg.exe"):
                return str(candidate.parent)
    return None


# pydub's own from_file()/mediainfo_json() resolve ffmpeg/ffprobe via a bare
# shutil.which("ffprobe") lookup every call, ignoring AudioSegment.converter.
# Extending this process's PATH is what actually makes both resolvable.
_ffmpeg_bin_dir = _find_ffmpeg_bin_dir()
if _ffmpeg_bin_dir:
    os.environ["PATH"] = _ffmpeg_bin_dir + os.pathsep + os.environ.get("PATH", "")


def concatenate_with_pauses(segments: list[tuple[str, int]], output_path: str) -> None:
    """segments: ordered list of (clip_path_or_empty, pause_ms_after).

    A clip_path of "" represents a standalone pause with no audio before it.
    """
    combined = AudioSegment.empty()
    for clip_path, pause_after_ms in segments:
        if clip_path:
            combined += AudioSegment.from_file(clip_path)
        if pause_after_ms:
            combined += AudioSegment.silent(duration=pause_after_ms)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    combined.export(output_path, format="mp3")
