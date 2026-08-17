import streamlit as st
from frontend.utils import asset_exists, pdf_bytes, pdf_view_button, render_html


def render_resume_cta():
    has_resume = asset_exists("assets/resume.pdf")

    if not has_resume:
        render_html("""
        <div id="resume-cta" class="pf-wrap" style="padding: 40px 0 0;">
          <div class="pf-resume-cta">
            <h3>Want the complete story?</h3>
            <p>The portfolio tells it visually — the resume has the full detail.</p>
            <p style="color:rgba(250,250,249,0.5);font-size:13px;">Add assets/resume.pdf to enable these buttons.</p>
          </div>
        </div>
        """)
        return

    render_html("""
    <div id="resume-cta" class="pf-wrap" style="padding: 40px 0 0;">
      <div class="pf-resume-cta">
        <h3>Want the complete story?</h3>
        <p>The portfolio tells it visually — the resume has the full details.</p>
      </div>
    </div>
    """)

    # View + Download rendered as one grouped, centered row directly under
    # the card -- both real Streamlit widgets so neither can sit inside the
    # HTML card itself, but keeping them adjacent here (rather than one in
    # the card and one floating below it) is what makes them read as a pair.
    render_html('<div style="height:14px;"></div>')
    spacer_l, col1, col2, spacer_r = st.columns([2, 3, 3, 2])
    with col1:
        pdf_view_button("View Resume", "assets/resume.pdf", "Resume", key="footer-view-resume")
    with col2:
        st.download_button(
            "Download (PDF)",
            data=pdf_bytes("assets/resume.pdf"),
            file_name="Abhimanyu_Saklani_Resume.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="footer-download-resume",
        )


def render_contact(profile: dict):
    links = f"""
      <a class="pf-btn pf-btn-primary" href="mailto:{profile['email']}">Email Me</a>
      <a class="pf-btn pf-btn-secondary" href="{profile['linkedin']}" target="_blank">LinkedIn</a>
      <a class="pf-btn pf-btn-secondary" href="{profile['github']}" target="_blank">GitHub</a>
    """
    render_html(f"""
    <div id="contact" class="pf-wrap pf-contact">
      <div class="pf-eyebrow">08 — Contact</div>
      <h2 class="pf-contact-title">Let's build something meaningful.</h2>
      <div class="pf-contact-links">{links}</div>
    </div>
    """)


def render_footer(profile: dict):
    render_html(f"""
    <div class="pf-wrap pf-footer">
      <div>© {profile['name']}</div>
      <div>{profile['location']}</div>
    </div>
    """)
