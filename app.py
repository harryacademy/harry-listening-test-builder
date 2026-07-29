"""Streamlit UI for building and rendering EN/VI listening-test audio."""

import re
from datetime import date
from pathlib import Path

import streamlit as st

from audio.mixer import concatenate_with_pauses
from config import DEFAULT_FILENAME_PATTERN, OUTPUT_DIR, SCRIPTS_DIR, TEMP_DIR
from scripts.models import Script, ScriptLine
from scripts.storage import list_saved_scripts, load_script, save_script
from tts.base import Voice
from tts.registry import available_providers, get_provider
from ui_theme import inject_theme, render_header, render_sidebar_logo

st.set_page_config(
    page_title="Harry Academy — Listening Test Audio Builder",
    page_icon=str(Path(__file__).parent / "assets" / "harry-academy-monogram.png"),
    layout="wide",
)

_FILENAME_UNSAFE_RE = re.compile(r'[<>:"/\\|?*]')


def safe_filename(name: str) -> str:
    return _FILENAME_UNSAFE_RE.sub("_", name).strip() or "output"


# ---------------------------------------------------------------- session --

def init_session_state():
    if "script" not in st.session_state:
        st.session_state.script = Script(
            name="untitled",
            mode="multi",
            filename_pattern=DEFAULT_FILENAME_PATTERN,
            lines=[ScriptLine(kind="speech", role="Speaker A")],
        )
    if "single_voice_id" not in st.session_state:
        st.session_state.single_voice_id = None


def sync_lines_from_widgets():
    """Pull current widget values back into the Script's line objects."""
    script: Script = st.session_state.script
    for line in script.lines:
        if line.kind == "speech":
            role_key = f"role_{line.id}"
            voice_key = f"voice_{line.id}"
            text_key = f"text_{line.id}"
            if role_key in st.session_state:
                line.role = st.session_state[role_key]
            if voice_key in st.session_state:
                line.voice_id = st.session_state[voice_key]
            if text_key in st.session_state:
                line.text = st.session_state[text_key]
        else:  # pause
            pause_key = f"pauseval_{line.id}"
            if pause_key in st.session_state:
                line.pause_ms = st.session_state[pause_key]


# ----------------------------------------------------------- row actions --

def move_line(line_id: str, direction: int):
    sync_lines_from_widgets()
    lines = st.session_state.script.lines
    idx = next(i for i, l in enumerate(lines) if l.id == line_id)
    new_idx = idx + direction
    if 0 <= new_idx < len(lines):
        lines[idx], lines[new_idx] = lines[new_idx], lines[idx]


def delete_line(line_id: str):
    sync_lines_from_widgets()
    lines = st.session_state.script.lines
    st.session_state.script.lines = [l for l in lines if l.id != line_id]


def add_speech_line():
    sync_lines_from_widgets()
    default_role = "Speaker A" if not st.session_state.script.lines else ""
    st.session_state.script.lines.append(ScriptLine(kind="speech", role=default_role))


def add_pause_line():
    sync_lines_from_widgets()
    st.session_state.script.lines.append(ScriptLine(kind="pause", pause_ms=500))


def new_script():
    st.session_state.script = Script(
        name="untitled",
        mode=st.session_state.script.mode if "script" in st.session_state else "multi",
        filename_pattern=DEFAULT_FILENAME_PATTERN,
        lines=[ScriptLine(kind="speech", role="Speaker A")],
    )


# ------------------------------------------------------------- voice data --

@st.cache_data(show_spinner="Fetching voice list from edge-tts...")
def load_voices(provider_name: str) -> list[Voice]:
    return get_provider(provider_name).list_voices()


def synthesize_preview(provider_name: str, voice: Voice) -> Path:
    sample_text = (
        "This is a preview of this voice."
        if voice.language == "English"
        else "Đây là bản xem trước của giọng đọc này."
    )
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    preview_path = TEMP_DIR / f"preview_{voice.id}.mp3"
    if not preview_path.exists():
        get_provider(provider_name).synthesize(sample_text, voice.id, str(preview_path))
    return preview_path


# ------------------------------------------------------------------- UI ---

def render_voice_browser(provider_name: str, voices: list[Voice]):
    st.subheader("Voice Browser")
    languages = sorted({v.language for v in voices})
    col1, col2, col3 = st.columns(3)
    with col1:
        lang_filter = st.multiselect("Language", languages, default=languages, key="vb_lang")
    filtered = [v for v in voices if v.language in lang_filter]
    with col2:
        genders = sorted({v.gender for v in filtered})
        gender_filter = st.multiselect("Gender", genders, default=genders, key="vb_gender")
    filtered = [v for v in filtered if v.gender in gender_filter]
    with col3:
        accents = sorted({v.accent for v in filtered})
        accent_filter = st.multiselect("Accent", accents, default=accents, key="vb_accent")
    filtered = [v for v in filtered if v.accent in accent_filter]

    if any(v.language == "Vietnamese" for v in filtered) and len(
        [v for v in voices if v.language == "Vietnamese"]
    ) <= 2:
        st.caption(
            "Note: edge-tts currently offers only 2 Vietnamese voices "
            "(1 female, 1 male), both standard accent — no regional variety."
        )

    st.caption(f"{len(filtered)} voice(s) match the current filters.")
    for voice in filtered:
        c1, c2 = st.columns([5, 1])
        with c1:
            st.write(f"**{voice.display_name}**  \n`{voice.id}`")
        with c2:
            if st.button("Preview", key=f"preview_btn_{voice.id}"):
                try:
                    path = synthesize_preview(provider_name, voice)
                    st.session_state[f"preview_path_{voice.id}"] = str(path)
                except Exception as e:
                    st.error(f"Preview failed for {voice.id}: {e}")
        preview_path = st.session_state.get(f"preview_path_{voice.id}")
        if preview_path:
            st.audio(preview_path)


def render_script_builder(voices: list[Voice]):
    st.subheader("Script Builder")
    script: Script = st.session_state.script

    top1, top2, top3 = st.columns([2, 2, 3])
    with top1:
        script.name = st.text_input("Test name", value=script.name)
    with top2:
        mode_label = st.radio(
            "Mode",
            options=["Multi-speaker", "Single-speaker"],
            index=0 if script.mode == "multi" else 1,
            horizontal=True,
        )
        script.mode = "multi" if mode_label == "Multi-speaker" else "single"
    with top3:
        script.filename_pattern = st.text_input(
            "Output filename pattern",
            value=script.filename_pattern,
            help="Placeholders: {testname}, {date}",
        )

    voice_ids = [v.id for v in voices]
    voice_labels = {v.id: v.display_name for v in voices}
    default_voice_id = voice_ids[0] if voice_ids else ""

    if script.mode == "single":
        if not st.session_state.single_voice_id or st.session_state.single_voice_id not in voice_ids:
            st.session_state.single_voice_id = next(
                (v.id for v in voices if v.locale == "en-US"), default_voice_id
            )
        st.session_state.single_voice_id = st.selectbox(
            "Voice (used for all lines)",
            options=voice_ids,
            index=voice_ids.index(st.session_state.single_voice_id) if st.session_state.single_voice_id in voice_ids else 0,
            format_func=lambda vid: voice_labels.get(vid, vid),
        )

    st.markdown("---")

    for i, line in enumerate(script.lines):
        with st.container(border=True, key=f"row_{line.id}"):
            if line.kind == "speech":
                cols = st.columns([2, 3, 5, 1, 1, 1])
                if script.mode == "multi":
                    cols[0].text_input("Role", value=line.role, key=f"role_{line.id}")
                    default_vidx = voice_ids.index(line.voice_id) if line.voice_id in voice_ids else (
                        voice_ids.index(default_voice_id) if default_voice_id in voice_ids else 0
                    )
                    cols[1].selectbox(
                        "Voice",
                        options=voice_ids,
                        index=default_vidx,
                        format_func=lambda vid: voice_labels.get(vid, vid),
                        key=f"voice_{line.id}",
                    )
                else:
                    cols[0].caption(f"Line {i + 1}")
                    cols[1].caption("(uses single voice above)")
                cols[2].text_area("Text", value=line.text, key=f"text_{line.id}", height=80, label_visibility="visible" if i == 0 else "collapsed")
                cols[3].button("↑", key=f"up_{line.id}", on_click=move_line, args=(line.id, -1), disabled=(i == 0))
                cols[4].button("↓", key=f"down_{line.id}", on_click=move_line, args=(line.id, 1), disabled=(i == len(script.lines) - 1))
                cols[5].button("🗑", key=f"del_{line.id}", on_click=delete_line, args=(line.id,))
            else:  # pause row
                cols = st.columns([2, 3, 5, 1, 1, 1])
                cols[0].markdown("⏸ **Pause**")
                cols[1].number_input(
                    "Duration (ms)", min_value=0, max_value=60000, step=100,
                    value=line.pause_ms, key=f"pauseval_{line.id}", label_visibility="collapsed",
                )
                cols[2].write("")
                cols[3].button("↑", key=f"up_{line.id}", on_click=move_line, args=(line.id, -1), disabled=(i == 0))
                cols[4].button("↓", key=f"down_{line.id}", on_click=move_line, args=(line.id, 1), disabled=(i == len(script.lines) - 1))
                cols[5].button("🗑", key=f"del_{line.id}", on_click=delete_line, args=(line.id,))

    b1, b2, _ = st.columns([1, 1, 4])
    b1.button("+ Add line", on_click=add_speech_line)
    b2.button("+ Add pause", on_click=add_pause_line)


def render_save_load():
    st.subheader("Save / Load Script")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save current script"):
            sync_lines_from_widgets()
            path = save_script(st.session_state.script, SCRIPTS_DIR)
            st.success(f"Saved to {path}")
        if st.button("New blank script"):
            new_script()
            st.rerun()
    with col2:
        saved = list_saved_scripts(SCRIPTS_DIR)
        if saved:
            chosen = st.selectbox("Load saved script", options=saved, format_func=lambda p: p.stem)
            if st.button("Load selected"):
                st.session_state.script = load_script(chosen)
                st.rerun()
        uploaded = st.file_uploader("...or upload a script JSON", type=["json"])
        if uploaded is not None and st.button("Load uploaded file"):
            import json
            st.session_state.script = Script.from_dict(json.loads(uploaded.read().decode("utf-8")))
            st.rerun()


def render_generate(provider_name: str, voices: list[Voice]):
    st.subheader("Generate Audio")
    sync_lines_from_widgets()
    script: Script = st.session_state.script

    if st.button("Generate Audio", type="primary"):
        speech_lines = [l for l in script.lines if l.kind == "speech"]
        if not speech_lines:
            st.error("Add at least one line of text before generating.")
            return
        missing_text = [l for l in speech_lines if not l.text.strip()]
        if missing_text:
            st.error("One or more speech lines have empty text. Fill them in or delete the row.")
            return

        provider = get_provider(provider_name)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        progress = st.progress(0.0, text="Starting...")
        segments: list[tuple[str, int]] = []
        temp_files: list[Path] = []

        try:
            for i, line in enumerate(script.lines):
                if line.kind == "pause":
                    segments.append(("", line.pause_ms))
                    continue

                voice_id = st.session_state.single_voice_id if script.mode == "single" else line.voice_id
                if not voice_id:
                    st.error(f"Line '{line.text[:30]}...' has no voice assigned.")
                    return

                clip_path = TEMP_DIR / f"line_{line.id}.mp3"
                progress.progress(i / len(script.lines), text=f"Rendering line {i + 1}/{len(script.lines)}...")
                try:
                    provider.synthesize(line.text, voice_id, str(clip_path))
                except Exception as e:
                    st.error(
                        f"Failed to synthesize line {i + 1} ({line.role or 'line'}): {e}\n\n"
                        "Check your internet connection (edge-tts requires network access "
                        "for each synthesis call) and that the text doesn't contain unsupported content."
                    )
                    return

                temp_files.append(clip_path)
                segments.append((str(clip_path), 0))

            progress.progress(0.95, text="Mixing final audio...")
            date_str = date.today().isoformat()
            filename = safe_filename(
                script.filename_pattern.format(testname=safe_filename(script.name), date=date_str)
            )
            if not filename.lower().endswith(".mp3"):
                filename += ".mp3"
            output_path = OUTPUT_DIR / filename

            try:
                concatenate_with_pauses(segments, str(output_path))
            except Exception as e:
                st.error(
                    f"Failed to mix audio: {e}\n\n"
                    "Make sure ffmpeg is installed and on PATH (required by pydub)."
                )
                return

            progress.progress(1.0, text="Done.")
            st.success(f"Generated: {output_path}")
            st.audio(str(output_path))
            with open(output_path, "rb") as f:
                st.download_button("Download MP3", data=f.read(), file_name=filename, mime="audio/mpeg")
        finally:
            for tf in temp_files:
                try:
                    tf.unlink(missing_ok=True)
                except OSError:
                    pass


# ------------------------------------------------------------------ main --

def main():
    init_session_state()
    inject_theme()
    render_header()

    render_sidebar_logo()
    provider_name = st.sidebar.selectbox("TTS Provider", options=available_providers(), index=0)
    if st.sidebar.button("Refresh voice list"):
        load_voices.clear()

    try:
        voices = load_voices(provider_name)
    except Exception as e:
        st.error(
            f"Could not fetch voice list from {provider_name}: {e}\n\n"
            "This requires an internet connection. Check your network and click "
            "'Refresh voice list' in the sidebar to retry."
        )
        return

    with st.expander("Voice Browser", expanded=False):
        render_voice_browser(provider_name, voices)

    render_script_builder(voices)
    st.markdown("---")
    render_save_load()
    st.markdown("---")
    render_generate(provider_name, voices)


if __name__ == "__main__":
    main()
