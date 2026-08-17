from frontend.utils import render_html


def render(education: list, standalone: bool = False):
    section_class = "pf-section-standalone" if standalone else "pf-section"
    items_html = ""
    for edu in education:
        coursework_html = ""
        if edu.get("coursework"):
            coursework_html = f"""
            <div class="pf-bullet-label">Coursework</div>
            <div class="pf-coursework">{" · ".join(edu["coursework"])}</div>
            """

        detail_html = ""
        if edu.get("detail"):
            detail_html = f'<div class="pf-edu-detail">{edu["detail"]}</div>'

        items_html += f"""
        <div class="pf-timeline-item pf-reveal">
          <div class="pf-timeline-dot"></div>
          <div class="pf-role-title">{edu["institution"]}</div>
          <div class="pf-role-company">{edu["degree"]}</div>
          <div class="pf-role-meta">{edu["location"]} · {edu["dates"]}</div>
          {detail_html}
          {coursework_html}
        </div>
        """

    render_html(f"""
    <div id="education" class="{section_class} pf-wrap">
      <div class="pf-section-head">
        <div class="pf-eyebrow">02 — Education</div>
        <h2 class="pf-section-title">How I got here.</h2>
      </div>
      <div class="pf-timeline">{items_html}</div>
    </div>
    """)