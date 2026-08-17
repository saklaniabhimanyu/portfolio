from frontend.utils import render_html


def render(projects: list, standalone: bool = False):
    if not projects:
        return
    section_class = "pf-section-standalone" if standalone else "pf-section"

    cards_html = ""
    for project in projects:
        tech = " · ".join(project.get("technologies", []))
        actions = f'<a class="pf-btn pf-btn-secondary pf-btn-small" href="?project={project["id"]}" target="_self">Details</a>'
        if project.get("github"):
            actions += f'<a class="pf-btn pf-btn-secondary pf-btn-small" href="{project["github"]}" target="_blank">GitHub</a>'

        cards_html += f"""
        <div class="pf-academic-card pf-reveal">
          <div class="pf-academic-title">{project["title"]}</div>
          <div class="pf-academic-tagline">{project["tagline"]}</div>
          <div class="pf-academic-tech">{tech}</div>
          <div class="pf-card-actions">{actions}</div>
        </div>
        """

    render_html(f"""
    <div id="academic-projects" class="{section_class} pf-wrap">
      <div class="pf-section-head">
        <div class="pf-eyebrow">06 — Academic & Coursework Projects</div>
        <h2 class="pf-section-title">Also built.</h2>
      </div>
      <div class="pf-academic-grid">{cards_html}</div>
    </div>
    """)