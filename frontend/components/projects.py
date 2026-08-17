import re
from frontend.utils import image_tag_or_placeholder, render_html


def _headline_metric(results: list) -> str:
    """Pull the single most prominent metric out of a project's results
    for the compact card badge -- the full stat sheet lives on the detail page."""
    if not results:
        return ""
    match = re.search(r"(\d[\d.,–\-]*\s?%?|R²\s?=\s?[\d.]+)", results[0])
    figure = match.group(0) if match else ""
    return f"{figure} — {results[0]}" if figure else results[0]


def render(projects: list, standalone: bool = False):
    section_class = "pf-section-standalone" if standalone else "pf-section"

    cards_html = ""
    for project in projects:
        tech_html = "".join(f'<span class="pf-card-tech-chip">{t}</span>' for t in project.get("technologies", []))
        image_inner = image_tag_or_placeholder(project.get("hero_image", ""), label="Add hero.png")

        metric = _headline_metric(project.get("results", []))
        metric_html = f'<div class="pf-card-metric">{metric}</div>' if metric else ""

        actions = f'<a class="pf-btn pf-btn-primary pf-btn-small" href="?project={project["id"]}" target="_self">View Details</a>'
        if project.get("github"):
            actions += f'<a class="pf-btn pf-btn-secondary pf-btn-small" href="{project["github"]}" target="_blank">GitHub</a>'

        cards_html += f"""
        <div class="pf-card pf-reveal">
          <div class="pf-card-image">{image_inner}</div>
          <div class="pf-card-body">
            <div class="pf-card-title">{project["title"]}</div>
            <div class="pf-card-tagline">{project["tagline"]}</div>
            {metric_html}
            <div class="pf-card-tech-row">{tech_html}</div>
            <div class="pf-card-actions">{actions}</div>
          </div>
        </div>
        """

    render_html(f"""
    <div id="projects" class="{section_class} pf-wrap" style="border-bottom:none;">
      <div class="pf-section-head">
        <div class="pf-eyebrow">05 — Projects</div>
        <h2 class="pf-section-title">Selected work.</h2>
      </div>
      <div class="pf-project-grid">{cards_html}</div>
    </div>
    """)