from frontend.utils import render_html


def render(profile: dict, standalone: bool = False):
    paragraphs = "".join(f"<p>{p}</p>" for p in profile["about_narrative"])
    info = profile["info_panel"]
    section_class = "pf-section-standalone" if standalone else "pf-section"

    info_rows = "".join(
        f"""
        <div class="pf-info-row">
          <div class="pf-info-label">{label}</div>
          <div class="pf-info-value">{value}</div>
        </div>
        """
        for label, value in [
            ("Location", info.get("location", "")),
            ("Focus", info.get("focus", "")),
            ("Current Role", info.get("current_role", "")),
            ("Education", info.get("education", "")),
        ]
        if value
    )

    render_html(f"""
    <div id="about" class="{section_class} pf-wrap">
      <div class="pf-section-head">
        <div class="pf-eyebrow">01 — About</div>
        <h2 class="pf-section-title">The short version.</h2>
      </div>
      <div class="pf-about-grid">
        <div class="pf-about-copy">{paragraphs}</div>
        <div class="pf-info-panel pf-reveal">{info_rows}</div>
      </div>
    </div>
    """)