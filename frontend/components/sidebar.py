import streamlit as st
from frontend.utils import (
    asset_exists, avatar_html, brand_icon_html, github_icon_html,
    linkedin_icon_html, mail_icon_html, pdf_view_button, render_html,
)


SECTIONS = [
    ("Home", ""),
    ("About", "about"),
    ("Education", "education"),
    ("Experience", "experience"),
    ("Skills", "skills"),
    ("Projects", "projects"),
    ("Academic Projects", "academic-projects"),
    ("Achievements", "achievements"),
    ("Contact", "contact"),
]


def render_top_nav():
    # render_html (not raw st.markdown) is required here: a plain
    # st.markdown call with an indented multi-line string makes Streamlit's
    # markdown parser treat 4+ leading spaces as a fenced code block, so
    # the nav prints as literal text instead of rendering as real links.
    render_html("""
    <div class="pf-top-nav">
        <div class="pf-top-nav-left">
            <a href="?" target="_self">Home</a>
            <a href="?section=about" target="_self">About</a>
            <a href="?section=contact" target="_self">Contact</a>
        </div>
    </div>
    """)


def render(profile: dict):
    photo_html = (
        f'<div style="margin-bottom:16px;">'
        f'{avatar_html(profile["name"], size=64, dark=True)}'
        f'</div>'
    )

    nav_links = "".join(
        f'<a href="?{"section=" + anchor if anchor else ""}" target="_self">{label}</a>'
        for label, anchor in SECTIONS
    )

    contact_links = [
        f'<a href="mailto:{profile["email"]}">{mail_icon_html()}{profile["email"]}</a>',
        f'<a href="{profile["linkedin"]}" target="_blank">{linkedin_icon_html()}LinkedIn</a>',
        f'<a href="{profile["github"]}" target="_blank">{github_icon_html()}GitHub</a>',
    ]

    if profile.get("leetcode"):
        contact_links.append(
            f'<a href="{profile["leetcode"]}" target="_blank">{brand_icon_html("leetcode", color="B5B3AC")}LeetCode</a>'
        )

    if profile.get("kaggle"):
        contact_links.append(
            f'<a href="{profile["kaggle"]}" target="_blank">{brand_icon_html("kaggle", color="B5B3AC")}Kaggle</a>'
        )

    with st.sidebar:
        render_html(f"""
            {photo_html}

            <div class="pf-sidebar-name">
                {profile["name"]}
            </div>

            <div class="pf-sidebar-role">
                {profile["title"]}
            </div>

            <div class="pf-sidebar-nav">
                {nav_links}
            </div>

            <hr class="pf-sidebar-divider" />

            <div class="pf-sidebar-label">
                Contact
            </div>

            <div class="pf-sidebar-contact">
                {"".join(contact_links)}
            </div>
        """)

        if asset_exists("assets/resume.pdf"):
            pdf_view_button(
                "View Resume",
                "assets/resume.pdf",
                "Resume",
                key="sidebar-view-resume",
            )
