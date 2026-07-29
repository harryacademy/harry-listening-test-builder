"""App-wide defaults."""

from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
SCRIPTS_DIR = BASE_DIR / "data" / "saved_scripts"
TEMP_DIR = BASE_DIR / "output" / ".tmp"

DEFAULT_FILENAME_PATTERN = "{testname}_{date}.mp3"
DEFAULT_PAUSE_MS = 500
