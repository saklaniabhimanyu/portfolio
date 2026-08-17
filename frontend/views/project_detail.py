import re
import streamlit as st
from frontend.utils import asset_exists, image_tag_or_placeholder, pdf_bytes, pdf_view_button, render_html


def _stat_sheet(results: list) -> str:
    if not results:
        return ""
    rows = ""
    for r in results:
        match = re.search(r"(\d[\d.,–\-]*\s?%?|R²\s?=\s?[\d.]+)", r)
        figure = match.group(0) if match else "→"
        rows += f"""
        <div class="pf-stat-row">
          <div class="pf-stat-figure">{figure}</div>
          <div class="pf-stat-desc">{r}</div>
        </div>
        """
    return f'<div class="pf-stat-sheet">{rows}</div>'


def _screenshot_path_and_caption(shot):
    """Screenshots can be a plain path string, or {'path': ..., 'caption': ...}
    for an optional one-line description under the image."""
    if isinstance(shot, dict):
        return shot.get("path", ""), shot.get("caption", "")
    return shot, ""


def render(project: dict):
    tech_html = "".join(f'<span class="pf-tech-chip">{t}</span>' for t in project.get("technologies", []))
    if project.get("models"):
        tech_html += "".join(f'<span class="pf-tech-chip">{m}</span>' for m in project["models"])

    links_html = ""
    if project.get("github"):
        links_html += f'<a class="pf-btn pf-btn-secondary pf-btn-small" href="{project["github"]}" target="_blank">GitHub</a>'
    if project.get("demo"):
        links_html += f'<a class="pf-btn pf-btn-secondary pf-btn-small" href="{project["demo"]}" target="_blank">Live Demo</a>'
    if not links_html:
        links_html = '<span style="font-family:var(--font-mono);font-size:12px;color:var(--muted);">No public repo or demo link yet</span>'

    # Build numbered sections dynamically -- academic projects often only have
    # a title/tagline/tech, so empty problem/solution/contribution/results
    # sections are skipped rather than rendered blank.
    sections_html = ""
    n = 1

    def add_section(label, body_html):
        nonlocal sections_html, n
        sections_html += f'<div class="pf-project-num" style="margin-top:40px;">0{n} — {label}</div>{body_html}'
        n += 1

    if project.get("problem"):
        add_section("The Problem", f'<p class="pf-project-desc">{project["problem"]}</p>')
    if project.get("solution"):
        add_section("The Solution", f'<p class="pf-project-desc">{project["solution"]}</p>')
    if project.get("contribution"):
        add_section("My Contribution", f'<p class="pf-project-desc">{project["contribution"]}</p>')
    if project.get("results"):
        add_section("Results", _stat_sheet(project["results"]))
    if not project.get("problem") and not project.get("solution"):
        add_section("Description", f'<p class="pf-project-desc">{project.get("description", "")}</p>')

    render_html(f"""
    <div class="pf-wrap" style="padding-top:56px;">
      <a href="?" target="_self" style="font-family:var(--font-mono);font-size:13px;color:var(--muted);">← Back to portfolio</a>

      <div style="margin-top:32px;">
        <div class="pf-project-num">Overview</div>
        <h1 class="pf-project-title">{project["title"]}</h1>
        <p class="pf-project-tagline">{project["tagline"]}</p>
        <div class="pf-tech-row" style="margin-bottom:24px;">{tech_html}</div>
        <div class="pf-project-actions" style="margin-bottom:36px;">{links_html}</div>
      </div>

      <div class="pf-project-image">{image_tag_or_placeholder(project.get("hero_image", ""), "Add hero.png")}</div>

      {sections_html}
    </div>
    """)

    screenshots = [_screenshot_path_and_caption(s) for s in project.get("screenshots", [])]
    screenshots = [(p, c) for p, c in screenshots if asset_exists(p)]
    if screenshots:
        render_html(f'<div class="pf-wrap"><div class="pf-project-num" style="margin-top:40px;">0{n} — Screenshots</div></div>')
        n += 1
        cols = st.columns(2)
        for i, (shot_path, caption) in enumerate(screenshots):
            with cols[i % 2]:
                full_path = str((__import__("pathlib").Path(__file__).resolve().parent.parent.parent / shot_path))
                if caption:
                    st.image(full_path, caption=caption)
                else:
                    st.image(full_path)

    case_study = project.get("case_study", "")
    if case_study and asset_exists(case_study):
        render_html(f'<div id="case-study" class="pf-wrap"><div class="pf-project-num" style="margin-top:40px;">0{n} — Case Study</div></div>')
        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            pdf_view_button("View", case_study, f"{project['title']} — Case Study", key=f"case-view-{project['id']}", use_container_width=True)
        with col2:
            st.download_button(
                "Download",
                data=pdf_bytes(case_study),
                file_name=f"{project['id']}-case-study.pdf",
                mime="application/pdf",
                key=f"case-dl-{project['id']}",
                use_container_width=True,
            )

    render_html('<div class="pf-wrap" style="height:80px;"></div>')
