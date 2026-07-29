"""Harry Academy design system applied to the Streamlit chrome.

Tokens pulled live from the "Harry Academy Design System" DesignSync project
(colors.css, typography.css, spacing.css, fonts.css) and copied wholesale —
see that project's readme.md for the reasoning behind each token.
"""

import base64
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).parent / "assets"

# ---- tokens/fonts.css ----
_FONTS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');
"""

# ---- tokens/colors.css ----
_COLORS_CSS = """
:root {
  --blue-50:  #eaf9fe;
  --blue-100: #cdf1fc;
  --blue-200: #9de4f8;
  --blue-300: #64d3f2;
  --blue-400: #38c1ea;
  --blue-500: #1fb0de;
  --blue-600: #128fbb;
  --blue-700: #0e7093;
  --blue-800: #0d5877;
  --blue-900: #0b4560;

  --ink-0:   #ffffff;
  --ink-50:  #f7f7f8;
  --ink-100: #eceef0;
  --ink-200: #d8dbdf;
  --ink-300: #b7bcc3;
  --ink-400: #888f99;
  --ink-500: #5c6570;
  --ink-600: #3f4650;
  --ink-700: #292e35;
  --ink-800: #16191d;
  --ink-900: #0a0b0e;

  --surface-page:      var(--ink-0);
  --surface-page-sunk: var(--ink-50);
  --surface-card:      var(--ink-0);
  --surface-inverse:   var(--ink-900);
  --surface-brand:     var(--blue-500);
  --surface-brand-soft:var(--blue-50);

  --text-heading: var(--ink-900);
  --text-body:    var(--ink-700);
  --text-muted:   var(--ink-500);
  --text-faint:   var(--ink-400);
  --text-on-brand:  var(--ink-0);
  --text-on-inverse:var(--ink-0);
  --text-link:      var(--blue-600);
  --text-link-hover:var(--blue-700);

  --border-subtle: var(--ink-100);
  --border-default:var(--ink-200);
  --border-strong: var(--ink-400);
  --border-brand:  var(--blue-400);

  --action-primary:        var(--ink-900);
  --action-primary-hover:  var(--ink-800);
  --action-primary-active: var(--ink-700);
  --action-brand:          var(--blue-500);
  --action-brand-hover:    var(--blue-600);
  --action-brand-active:   var(--blue-700);
  --action-disabled-bg:    var(--ink-100);
  --action-disabled-fg:    var(--ink-400);

  --state-success:      #1e9e6b;
  --state-success-soft: #e6f6ef;
  --state-warning:      #c98a1c;
  --state-warning-soft: #fbf1de;
  --state-danger:       #d1443a;
  --state-danger-soft:  #fbe9e7;
  --state-info:         var(--blue-500);
  --state-info-soft:    var(--blue-50);

  --focus-ring: var(--blue-400);
}
"""

# ---- tokens/typography.css ----
_TYPOGRAPHY_CSS = """
:root {
  --font-display: "Playfair Display", "Times New Roman", serif;
  --font-body:    "Be Vietnam Pro", -apple-system, "Segoe UI", sans-serif;
  --font-mono:    "IBM Plex Mono", ui-monospace, "SFMono-Regular", monospace;

  --text-display-xl: 72px;
  --text-display-lg: 56px;
  --text-display-md: 40px;
  --text-display-sm: 32px;
  --text-h1: 28px;
  --text-h2: 24px;
  --text-h3: 20px;
  --text-body-lg: 18px;
  --text-body-md: 16px;
  --text-body-sm: 14px;
  --text-caption: 12px;

  --leading-display: 1.08;
  --leading-heading: 1.2;
  --leading-body: 1.6;
  --leading-tight: 1.3;

  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;

  --tracking-tight: -0.01em;
  --tracking-normal: 0;
  --tracking-wide: 0.04em;
  --tracking-badge: 0.18em;
}
"""

# ---- tokens/spacing.css ----
_SPACING_CSS = """
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-32: 128px;

  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-full: 999px;

  --shadow-xs: 0 1px 2px rgba(10, 11, 14, 0.06);
  --shadow-sm: 0 2px 6px rgba(10, 11, 14, 0.08);
  --shadow-md: 0 8px 24px rgba(10, 11, 14, 0.10);
  --shadow-lg: 0 16px 40px rgba(10, 11, 14, 0.14);
  --shadow-focus: 0 0 0 3px rgba(31, 176, 222, 0.35);

  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --duration-fast: 120ms;
  --duration-base: 180ms;
  --duration-slow: 280ms;

  --container-max: 1200px;
  --border-width: 1px;
}
"""

# Component-level overrides mapping Streamlit's DOM (data-testid attributes
# and BaseWeb data-baseweb hooks, verified live against the running app)
# onto the token set above. `st.container(border=True, key=f"row_{id}")`
# gets a stable `st-key-row_<id>` class Streamlit generates from `key=`;
# emotion-cache hash classes are NOT used here since those aren't stable.
_COMPONENT_CSS = """
.stApp {
  background: var(--surface-page-sunk);
}
[data-testid="stMainBlockContainer"] {
  max-width: var(--container-max);
}
.stApp, .stApp p, .stApp label,
.stApp span:not([data-testid="stIconMaterial"]),
.stApp div:not([data-testid="stIconMaterial"]) {
  font-family: var(--font-body);
}
/* Material icon ligatures (sidebar collapse arrow, expander chevron, etc.)
   must keep Streamlit's icon font or they render as literal text. */
[data-testid="stIconMaterial"] {
  font-family: "Material Symbols Rounded", "Material Icons" !important;
}
.stApp, .stApp p {
  color: var(--text-body);
}

[data-testid="stHeading"] h1,
[data-testid="stHeading"] h2,
[data-testid="stHeading"] h3,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
  font-family: var(--font-display) !important;
  color: var(--text-heading) !important;
  letter-spacing: var(--tracking-tight);
  font-weight: var(--weight-semibold) !important;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
  background: var(--ink-900) !important;
}
[data-testid="stSidebar"] * {
  color: rgba(255, 255, 255, 0.85) !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
  color: rgba(255, 255, 255, 0.55) !important;
  font-size: var(--text-body-sm);
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [role="group"] {
  background: rgba(255, 255, 255, 0.06) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] input[role="combobox"] {
  color: rgba(255, 255, 255, 0.9) !important;
}

/* ---- Buttons ---- */
/* Primary CTA (Generate Audio) uses brand blue, matching .btn-brand
   in the companion vocab app rather than the ink-black form-submit variant. */
[data-testid="stBaseButton-primary"] {
  background: var(--action-brand) !important;
  color: var(--text-on-brand) !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-weight: var(--weight-semibold) !important;
  transition: background var(--duration-base) var(--ease-standard),
              transform var(--duration-fast) var(--ease-standard);
}
[data-testid="stBaseButton-primary"]:hover {
  background: var(--action-brand-hover) !important;
}
[data-testid="stBaseButton-primary"]:active {
  transform: scale(0.97);
}

[data-testid="stBaseButton-secondary"] {
  background: var(--surface-card) !important;
  color: var(--text-heading) !important;
  border: 1px solid var(--border-default) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-weight: var(--weight-medium) !important;
  transition: background var(--duration-base) var(--ease-standard),
              border-color var(--duration-base) var(--ease-standard);
}
[data-testid="stBaseButton-secondary"]:hover {
  background: var(--surface-page-sunk) !important;
  border-color: var(--border-strong) !important;
}
[data-testid="stBaseButton-secondary"]:active {
  transform: scale(0.97);
}

[data-testid="stDownloadButton"] button {
  background: var(--surface-card) !important;
  color: var(--blue-700) !important;
  border: 1px solid var(--border-brand) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-weight: var(--weight-semibold) !important;
}
[data-testid="stDownloadButton"] button:hover {
  background: var(--surface-brand-soft) !important;
}

/* ---- Text inputs / textareas ---- */
[data-testid="stTextInputRootElement"],
[data-testid="stTextAreaRootElement"] {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border-default) !important;
  background: var(--surface-card) !important;
  transition: border-color var(--duration-base) var(--ease-standard),
              box-shadow var(--duration-base) var(--ease-standard);
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within {
  border-color: var(--border-brand) !important;
  box-shadow: var(--shadow-focus) !important;
}
[data-testid="stTextInputRootElement"] input,
[data-testid="stTextAreaRootElement"] textarea {
  font-family: var(--font-body) !important;
  color: var(--text-heading) !important;
}

/* ---- Multiselect chips (still BaseWeb in this Streamlit version) ---- */
[data-baseweb="select"] > div {
  border-radius: var(--radius-sm) !important;
  border-color: var(--border-default) !important;
  font-family: var(--font-body) !important;
}
[data-baseweb="tag"] {
  background: var(--surface-page-sunk) !important;
  border: 1px solid var(--border-default) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-body) !important;
}

/* ---- st.selectbox (React Aria ComboBox in this Streamlit version) ---- */
[data-testid="stSelectbox"] [role="group"] {
  border-radius: var(--radius-sm) !important;
  border-color: var(--border-default) !important;
  background: var(--surface-card) !important;
  transition: border-color var(--duration-base) var(--ease-standard),
              box-shadow var(--duration-base) var(--ease-standard);
}
[data-testid="stSelectbox"] [role="group"]:focus-within {
  border-color: var(--border-brand) !important;
  box-shadow: var(--shadow-focus) !important;
}
[data-testid="stSelectbox"] input[role="combobox"] {
  font-family: var(--font-body) !important;
  color: var(--text-heading) !important;
}

/* ---- Dropdown popovers (React Aria listbox/option, portal-rendered) ---- */
[role="listbox"] {
  font-family: var(--font-body) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow-md) !important;
}
[role="option"] {
  font-family: var(--font-body) !important;
}
[role="option"][aria-selected="true"] {
  background: var(--surface-brand-soft) !important;
  color: var(--blue-700) !important;
}

/* ---- Radio ---- */
[data-testid="stRadioGroup"] label {
  font-family: var(--font-body);
}
input[type="radio"], input[type="checkbox"] {
  accent-color: var(--blue-500);
}

/* ---- Expander ---- */
[data-testid="stExpander"] {
  background: var(--surface-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xs);
  overflow: hidden;
}

/* ---- Script row cards ---- */
[class*="st-key-row_"] {
  background: var(--surface-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  box-shadow: var(--shadow-xs) !important;
  padding: var(--space-4) !important;
  margin-bottom: var(--space-3) !important;
}

/* ---- Alerts (Toast pattern: tone-colored 3px left edge) ---- */
[data-testid="stAlertContainer"] {
  border-radius: var(--radius-sm) !important;
  border-left: 3px solid var(--ink-300) !important;
  font-family: var(--font-body) !important;
}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) {
  background: var(--state-success-soft) !important;
  border-left-color: var(--state-success) !important;
}
[data-testid="stAlertContentSuccess"] { color: var(--state-success) !important; }
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) {
  background: var(--state-danger-soft) !important;
  border-left-color: var(--state-danger) !important;
}
[data-testid="stAlertContentError"] { color: var(--state-danger) !important; }
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) {
  background: var(--state-warning-soft) !important;
  border-left-color: var(--state-warning) !important;
}
[data-testid="stAlertContentWarning"] { color: var(--state-warning) !important; }
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentInfo"]) {
  background: var(--state-info-soft) !important;
  border-left-color: var(--state-info) !important;
}
[data-testid="stAlertContentInfo"] { color: var(--blue-700) !important; }

/* ---- Progress ---- */
[data-testid="stProgressBarTrack"] {
  background: var(--surface-page-sunk) !important;
  border-radius: var(--radius-full) !important;
}
[data-testid="stProgress"] div[role="progressbar"] {
  background: var(--action-brand) !important;
}

/* ---- File uploader ---- */
[data-testid="stFileUploaderDropzone"] {
  background: var(--surface-page-sunk) !important;
  border: 1.5px dashed var(--border-default) !important;
  border-radius: var(--radius-md) !important;
}

/* ---- Captions ---- */
[data-testid="stCaptionContainer"] {
  color: var(--text-muted) !important;
  font-family: var(--font-body) !important;
}

/* ---- Masthead ---- */
.ha-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  background: var(--surface-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xs);
  padding: var(--space-5) var(--space-6);
  margin-bottom: var(--space-6);
}
.ha-header img {
  height: 42px;
  display: block;
}
.ha-header-text .ha-wordmark {
  font-family: var(--font-display);
  font-size: var(--text-h1);
  color: var(--text-heading);
  letter-spacing: var(--tracking-tight);
  line-height: var(--leading-heading);
  font-weight: var(--weight-semibold);
}
.ha-header-text .ha-wordmark em {
  font-style: normal;
  color: var(--blue-600);
}
.ha-header-text .ha-subtitle {
  font-family: var(--font-body);
  font-size: var(--text-body-sm);
  color: var(--text-muted);
  margin-top: 2px;
}

.ha-sidebar-logo {
  display: inline-block;
  background: #fff;
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  margin-bottom: var(--space-4);
}
.ha-sidebar-logo img {
  height: 20px;
  display: block;
}
"""


@st.cache_data(show_spinner=False)
def _load_logo_b64(filename: str) -> str:
    return base64.b64encode((ASSETS_DIR / filename).read_bytes()).decode("ascii")


def inject_theme():
    css = "\n".join([_FONTS_CSS, _COLORS_CSS, _TYPOGRAPHY_CSS, _SPACING_CSS, _COMPONENT_CSS])
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header():
    logo_b64 = _load_logo_b64("harry-academy-monogram.png")
    st.markdown(
        f"""
        <div class="ha-header">
            <img src="data:image/png;base64,{logo_b64}" alt="Harry Academy" />
            <div class="ha-header-text">
                <div class="ha-wordmark">Harry <em>Academy</em></div>
                <div class="ha-subtitle">Listening Test Audio Builder &middot; TOEIC / IELTS</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_logo():
    logo_b64 = _load_logo_b64("harry-academy-horizontal.png")
    st.sidebar.markdown(
        f"""
        <div class="ha-sidebar-logo">
            <img src="data:image/png;base64,{logo_b64}" alt="Harry Academy" />
        </div>
        """,
        unsafe_allow_html=True,
    )
