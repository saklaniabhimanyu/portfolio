import sys
from pathlib import Path

# Allow `python -m streamlit run frontend/app.py` to import the frontend package
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from frontend import data_loader
from frontend.utils import render_html
from frontend.components import (
    sidebar, hero, about, experience, projects, academic_projects,
    education, skills, achievements, footer,
)
from frontend.views import project_detail

st.set_page_config(
    page_title="Abhimanyu Saklani Portfolio",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    css_path = ROOT / "frontend" / "styles" / "main.css"
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Single-section pages instead of one long scrolling page with #anchor links.
# Anchor-scroll-on-load doesn't mix well with Streamlit: a sidebar click
# triggers a full browser navigation (new page load), and the browser tries
# to jump to the #fragment before Streamlit has finished progressively
# streaming the page's content in -- the result is landing at the wrong
# spot, or landing before layout has settled and seeing extra blank space
# where a not-yet-mounted element will go. Rendering exactly one section,
# starting at the very top of a fresh page, sidesteps the race entirely.
#
# standalone=True on every one of these: it swaps each section's top
# padding from the generous 120px meant to separate sections on the
# continuous home-page scroll down to a small amount, since on a
# standalone page that 120px was stacking redundantly on top of the
# back-link's own spacing above it.
SECTION_RENDERERS = {
    "home": lambda profile: render_home(profile),
    "about": lambda profile: about.render(profile, standalone=True),
    "education": lambda profile: education.render(data_loader.get_education(), standalone=True),
    "experience": lambda profile: experience.render(data_loader.get_experience(), standalone=True),
    "skills": lambda profile: skills.render(data_loader.get_skills(), standalone=True),
    "projects": lambda profile: projects.render(data_loader.get_projects(), standalone=True),
    "academic-projects": lambda profile: academic_projects.render(data_loader.get_academic_projects(), standalone=True),
    "achievements": lambda profile: achievements.render(data_loader.get_achievements()),
    "contact": lambda profile: footer.render_contact(profile),
}


def render_home(profile):
    hero.render(profile)
    about.render(profile)
    education.render(data_loader.get_education())
    experience.render(data_loader.get_experience())
    skills.render(data_loader.get_skills())
    projects.render(data_loader.get_projects())
    academic_projects.render(data_loader.get_academic_projects())
    achievements.render(data_loader.get_achievements())
    footer.render_resume_cta()
    footer.render_contact(profile)


def main():
    load_css()
    profile = data_loader.get_profile()

    sidebar.render(profile)
    sidebar.render_top_nav()
    query_params = st.query_params
    project_id = query_params.get("project")
    section = query_params.get("section")

    if project_id:
        project = data_loader.get_project(project_id)
        if project:
            project_detail.render(project)
        else:
            render_html('<div class="pf-wrap" style="padding-top:80px;">Project not found. <a href="?" target="_self">Back to portfolio</a></div>')
        footer.render_footer(profile)
        return

    if section and section in SECTION_RENDERERS:
        SECTION_RENDERERS[section](profile)
        footer.render_footer(profile)
        return

    render_home(profile)
    footer.render_footer(profile)


if __name__ == "__main__":
    main()