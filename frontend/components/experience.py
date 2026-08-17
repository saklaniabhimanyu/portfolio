from frontend.utils import render_html


def render(experience: list, standalone: bool = False):
    section_class = "pf-section-standalone" if standalone else "pf-section"
    items_html = ""
    for role in experience:
        what_html = "".join(f"<li>{b}</li>" for b in role.get("what_i_did", []))
        impact_html = ""
        if role.get("impact"):
            impact_bullets = "".join(f"<li>{b}</li>" for b in role["impact"])
            impact_html = f'<div class="pf-bullet-label">Impact</div><ul class="pf-bullets">{impact_bullets}</ul>'

        tech_html = "".join(f'<span class="pf-tech-chip">{t}</span>' for t in role.get("technologies", []))

        items_html += f"""
        <div class="pf-timeline-item pf-reveal">
          <div class="pf-timeline-dot"></div>
          <div class="pf-role-title">{role["role"]}</div>
          <div class="pf-role-company">{role["company"]} · {role["location"]}</div>
          <div class="pf-role-meta">{role["dates"]}</div>
          <div class="pf-bullet-label">What I Did</div>
          <ul class="pf-bullets">{what_html}</ul>
          {impact_html}
          <div class="pf-tech-row">{tech_html}</div>
        </div>
        """

    render_html(f"""
    <div id="experience" class="{section_class} pf-wrap">
      <div class="pf-section-head">
        <div class="pf-eyebrow">03 — Experience</div>
        <h2 class="pf-section-title">Where I've worked.</h2>
      </div>
      <div class="pf-timeline">{items_html}</div>
    </div>
    """)