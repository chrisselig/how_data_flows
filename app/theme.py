"""Corporate theme loader — shared, copyable across all HR course apps.

Portable bundle: copy this file together with the whole ``app/static/`` folder
into any course app, then call :func:`apply_theme` once, right after
``st.set_page_config()``::

    from app.theme import apply_theme
    ...
    st.set_page_config(...)
    apply_theme(default_name="My Course Title")

No third-party dependencies beyond Streamlit. To re-brand:

* Colours / background veil — edit the CSS variables in ``static/theme.css``.
* Logo — drop in ``static/logo.png`` (or ``.svg``).
* Background image — drop in ``static/background.png`` (or ``.jpg`` / ``.svg``).
* App/report name — set the ``APP_NAME`` environment variable per deployment;
  it overrides ``default_name``.
"""

from __future__ import annotations

import base64
import html
import os
from pathlib import Path

import streamlit as st

_STATIC_DIR = Path(__file__).parent / "static"

# First existing file wins (real assets before the committed placeholders).
_LOGO_CANDIDATES = ("logo.png", "logo.jpg", "logo.svg")
_BACKGROUND_CANDIDATES = ("background.png", "background.jpg", "background.svg")

_MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


def resolve_app_name(default_name: str = "Report") -> str:
    """Return the header title: ``APP_NAME`` env var, else ``default_name``."""
    return os.environ.get("APP_NAME", "").strip() or default_name


def _find_asset(candidates: tuple[str, ...]) -> Path | None:
    """Return the first existing static asset from ``candidates``."""
    for name in candidates:
        path = _STATIC_DIR / name
        if path.exists():
            return path
    return None


def _data_uri(path: Path) -> str:
    """Base64 data URI for an asset (works in any corporate env, no file server)."""
    mime = _MIME_BY_SUFFIX.get(path.suffix.lower(), "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{encoded}"


def apply_theme(default_name: str = "Report") -> None:
    """Inject the corporate CSS theme and render the branded header.

    Call once, immediately after ``st.set_page_config()``.

    The header shows the app/report name (orange, left) and the company logo
    (right) with a horizontal brand bar underneath. The title comes from the
    ``APP_NAME`` environment variable when set, otherwise ``default_name``.
    """
    css = (_STATIC_DIR / "theme.css").read_text()

    # Background image is injected as a CSS variable (kept out of theme.css so
    # the asset can be swapped without editing CSS). Falls back to the gradient
    # defined in theme.css when no background asset is present.
    background = _find_asset(_BACKGROUND_CANDIDATES)
    bg_override = (
        f":root {{ --app-bg-image: url('{_data_uri(background)}'); }}"
        if background is not None
        else ""
    )
    st.markdown(f"<style>{css}\n{bg_override}</style>", unsafe_allow_html=True)

    title = html.escape(resolve_app_name(default_name))
    logo = _find_asset(_LOGO_CANDIDATES)
    logo_html = (
        f'<img class="corp-logo" src="{_data_uri(logo)}" alt="Company logo" />'
        if logo is not None
        else ""
    )

    st.markdown(
        f'<div class="corp-header-bar">'
        f'<span class="corp-app-name">{title}</span>'
        f"{logo_html}"
        f"</div>"
        f'<hr class="corp-divider" />',
        unsafe_allow_html=True,
    )
