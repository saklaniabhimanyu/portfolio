from frontend.utils import render_html


def render(skills: list, standalone: bool = False):
    section_class = "pf-section-standalone" if standalone else "pf-section"
    rows_html = ""
    for group in skills:
        items = " · ".join(group["items"])
        rows_html += f"""
        <div class="pf-skill-row pf-reveal">
          <div class="pf-skill-num">{group["number"]}</div>
          <div class="pf-skill-cat">{group["category"]}</div>
          <div class="pf-skill-items">{items}</div>
        </div>
        """

    render_html(f"""
    <div id="skills" class="{section_class} pf-wrap">
      <div class="pf-section-head">
        <div class="pf-eyebrow">04 — Skills</div>
        <h2 class="pf-section-title">What I work with.</h2>
      </div>
      <div>{rows_html}</div>
    </div>
    """)