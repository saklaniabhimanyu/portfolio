"""
Small helpers for working with optional assets (images, PDFs) so the
site never renders a broken image tag or an empty button.
"""
import base64
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent


def render_html(html: str):
    """Render an HTML fragment via st.markdown.

    Every multi-line HTML string built from an indented Python f-string
    carries that indentation into the output. Streamlit's markdown parser
    treats 4+ leading spaces on a line as a fenced code block, so without
    stripping it the whole fragment prints as literal text instead of
    rendering. Always use this (not st.markdown directly) for HTML fragments.
    """
    cleaned = "\n".join(line.strip() for line in html.strip("\n").splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def asset_path(relative_path: str) -> Path:
    """relative_path is expected relative to the project root, e.g. 'assets/profile.jpg'."""
    return ROOT_DIR / relative_path


def asset_exists(relative_path: str) -> bool:
    if not relative_path:
        return False
    return asset_path(relative_path).is_file()


def image_to_base64(relative_path: str) -> str:
    path = asset_path(relative_path)
    with open(path, "rb") as f:
        data = f.read()
    ext = path.suffix.lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64,{base64.b64encode(data).decode()}"


def image_tag_or_placeholder(relative_path: str, label: str = "Add project image") -> str:
    """Returns an <img> tag if the asset exists, otherwise a labeled placeholder div.
    Caller is responsible for wrapping in the .pf-project-image container."""
    if asset_exists(relative_path):
        return f'<img src="{image_to_base64(relative_path)}" alt="{label}" />'
    return f"{label} — {relative_path}"


def initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    return "".join(p[0].upper() for p in parts[:2])


def avatar_html(name: str, size: int = 112, dark: bool = False, responsive: bool = False) -> str:
    """Round profile photo if assets/profile.jpg exists, otherwise a round
    placeholder (initials + dashed ring) so it's obvious where the photo goes.
    responsive=True fills its parent (sized by CSS) instead of a fixed px size --
    used for the large right-side hero portrait."""
    dim = "100%" if responsive else f"{size}px"
    if asset_exists("assets/profile.jpg"):
        return (
            f'<img src="{image_to_base64("assets/profile.jpg")}" alt="{name}" '
            f'style="width:{dim};height:{dim};border-radius:50%;object-fit:cover;'
            f'border:1px solid var(--hairline);" />'
        )
    ring_color = "rgba(250,250,249,0.25)" if dark else "var(--hairline)"
    text_color = "rgba(250,250,249,0.55)" if dark else "var(--muted)"
    font_size = max(14, size // 3) if not responsive else "clamp(24px, 8vw, 48px)"
    return f"""
    <div title="Add assets/profile.jpg to replace this placeholder"
         style="width:{dim};height:{dim};border-radius:50%;
                border:1.5px dashed {ring_color};
                display:flex;align-items:center;justify-content:center;
                font-family:var(--font-display);font-weight:600;
                font-size:{font_size};color:{text_color};
                flex-shrink:0;">
      {initials(name)}
    </div>
    """


def is_external_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def normalize_local_path(value: str) -> str:
    """Normalize a possibly-Windows-style local path (backslashes, as some
    editors write into JSON) into a forward-slash path."""
    return value.replace("\\", "/")


# Simple Icons (cdn.simpleicons.org) serves brand SVGs by slug + hex color,
# fetched by the visitor's own browser. Used only for the less-common brand
# marks (Kaggle, LeetCode) where a hand-written inline SVG risks looking
# subtly wrong. LinkedIn/GitHub/email are inline SVGs instead (below) --
# LinkedIn's icon wasn't rendering via this CDN, most likely because
# generic "social icon CDN" URL patterns are exactly what ad-blockers and
# privacy extensions (uBlock, Privacy Badger, etc.) commonly target, and a
# portfolio's icons shouldn't be at the mercy of the viewer's browser
# extensions. Colored to the site's muted gray by default so they sit
# quietly in the pills; CSS lifts them to full opacity on hover.
_BRAND_ICON_SLUGS = {
    "kaggle": "kaggle",
    "leetcode": "leetcode",
}


def brand_icon_html(name: str, size: int = 14, color: str = "62666F") -> str:
    slug = _BRAND_ICON_SLUGS.get(name)
    if not slug:
        return ""
    return (
        f'<img src="https://cdn.simpleicons.org/{slug}/{color}" width="{size}" height="{size}" '
        f'alt="" class="pf-brand-icon" loading="lazy" />'
    )


def _svg_icon(size, viewbox, path, stroke=False):
    if stroke:
        return (
            f'<svg class="pf-brand-icon" width="{size}" height="{size}" viewBox="{viewbox}" '
            f'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round">{path}</svg>'
        )
    return f'<svg class="pf-brand-icon" width="{size}" height="{size}" viewBox="{viewbox}" fill="currentColor">{path}</svg>'


def linkedin_icon_html(size: int = 14) -> str:
    return _svg_icon(size, "0 0 448 512",
        '<path d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 '
        '53.79 0 1 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.3 '
        '0-55.7 37.7-55.7 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.7-48.3 87.9-48.3 94 0 111.28 61.9 111.28 142.3V448z"/>')


def github_icon_html(size: int = 14) -> str:
    return _svg_icon(size, "0 0 16 16",
        '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
        '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
        '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 '
        '0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 '
        '2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 '
        '3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 '
        '8c0-4.42-3.58-8-8-8z"/>')


def mail_icon_html(size: int = 14) -> str:
    return _svg_icon(size, "0 0 24 24",
        '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>', stroke=True)


# A couple of generic (non-brand) glyphs, as small inline SVGs so they
# don't need a network round-trip.
_PHONE_SVG = (
    '<svg class="pf-brand-icon" width="{size}" height="{size}" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 '
    '19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 '
    '2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 '
    '2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
)


def phone_icon_html(size: int = 14) -> str:
    return _PHONE_SVG.format(size=size)


def pdf_bytes(relative_path: str):
    path = asset_path(relative_path)
    if not path.is_file():
        return None
    with open(path, "rb") as f:
        return f.read()


# --- PDF viewing -----------------------------------------------------------
#
# Two approaches were tried and both are fundamentally broken, not just buggy:
#
# 1. Streamlit's static file serving (frontend/static/, "app/static/...")
#    deliberately sends .pdf files with Content-Type: text/plain -- this is
#    an intentional Streamlit security decision (see their docs and
#    github.com/streamlit/streamlit/issues/9425), not something a config
#    change can fix. Browsers won't open their PDF viewer for a text/plain
#    response.
# 2. A data: URI opened via <a target="_blank"> is blocked outright by
#    Chrome ("Not allowed to navigate top frame to data URL") -- a hard
#    security restriction, not a quirk of our markup.
#
# So "view" is implemented by rendering the PDF's pages to images with
# PyMuPDF and showing them in a modal (st.dialog) -- no external server,
# no MIME issues, no data-URI restriction, and (unlike an inline expander)
# it doesn't add permanent height to the page since it's an overlay.
@st.cache_data(show_spinner=False)
def pdf_page_images(relative_path: str, dpi: int = 130):
    import pymupdf
    data = pdf_bytes(relative_path)
    doc = pymupdf.open(stream=data, filetype="pdf")
    zoom = dpi / 72
    matrix = pymupdf.Matrix(zoom, zoom)
    images = [page.get_pixmap(matrix=matrix).tobytes("png") for page in doc]
    doc.close()
    return images


@st.dialog("Document preview", width="large")
def _pdf_preview_dialog(relative_path: str, title: str):
    st.markdown(f"**{title}**")
    for page_png in pdf_page_images(relative_path):
        st.image(page_png, width='stretch')


def pdf_view_button(label: str, relative_path: str, title: str, key: str, use_container_width: bool = True):
    """A button that opens the given local PDF in a modal, rendered as
    page images. Safe to call even if the file doesn't exist -- the
    caller should still gate on asset_exists() to decide whether to show
    the button at all."""
    if st.button(label, key=key, use_container_width=use_container_width):
        _pdf_preview_dialog(relative_path, title)
