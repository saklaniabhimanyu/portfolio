import streamlit as st
from frontend.utils import (
    avatar_html, brand_icon_html, github_icon_html, linkedin_icon_html,
    mail_icon_html, phone_icon_html, render_html,
)
from frontend.components import ai_chat


def render(profile: dict):
    role_chips = "".join(f'<span class="pf-role-chip">{r}</span>' for r in profile.get("target_roles", []))

    contact_pills = [
        f'<a class="pf-contact-pill" href="mailto:{profile["email"]}">{mail_icon_html()}{profile["email"]}</a>',
        f'<a class="pf-contact-pill" href="tel:{profile["phone"].replace(" ", "")}">{phone_icon_html()}{profile["phone"]}</a>',
        f'<a class="pf-contact-pill" href="{profile["linkedin"]}" target="_blank">{linkedin_icon_html()}LinkedIn</a>',
        f'<a class="pf-contact-pill" href="{profile["github"]}" target="_blank">{github_icon_html()}GitHub</a>',
    ]
    if profile.get("leetcode"):
        contact_pills.append(f'<a class="pf-contact-pill" href="{profile["leetcode"]}" target="_blank">{brand_icon_html("leetcode")}LeetCode</a>')
    if profile.get("kaggle"):
        contact_pills.append(f'<a class="pf-contact-pill" href="{profile["kaggle"]}" target="_blank">{brand_icon_html("kaggle")}Kaggle</a>')

    render_html('<div id="home" class="pf-hero pf-fade-up"></div>')

    # Real st.columns (not a pure-CSS grid) on purpose: the "Ask about
    # myself" box needs to sit as an immediate sibling of the photo, inside
    # the same right-hand column, so it lands right below it instead of
    # appearing as a whole separate section further down the page.
    left_col, right_col = st.columns([65, 35], gap="small")

    with left_col:
        render_html(f"""
      <div class="pf-eyebrow">
        <span class="dot"></span>{profile.get("availability", "")}
      </div>

      <h1 class="pf-hero-name">{profile["name"]}</h1>

      <div class="pf-hero-role">{profile["title"]}</div>

      <div class="pf-contact-row pf-contact-row-primary">
        {contact_pills[0]}
        {contact_pills[1]}
      </div>

      <div class="pf-contact-row pf-contact-row-secondary">
        {contact_pills[2]}
        {contact_pills[3]}
        {contact_pills[4] if len(contact_pills) > 4 else ""}
        {contact_pills[5] if len(contact_pills) > 5 else ""}
      </div>

      <p class="pf-hero-summary">{profile["hero_summary"]}</p>

      <div class="pf-hero-actions">
        <a class="pf-btn pf-btn-primary" href="#projects" target="_self">
          View My Work
        </a>
      </div>

      <div class="pf-target-roles-label">Target Roles</div>
      <div class="pf-target-roles-row">{role_chips}</div>
      """)

    with right_col:
        photo_html = avatar_html(profile["name"], responsive=True)
        render_html(f'<div class="pf-hero-photo-col">{photo_html}</div>')
        ai_chat.render_inline()