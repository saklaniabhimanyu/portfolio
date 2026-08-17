import streamlit as st
from frontend.utils import (
    asset_exists, is_external_url, normalize_local_path,
    pdf_bytes, pdf_view_button, render_html,
)


def render(data: dict, standalone: bool = False):
    certs = data.get("certifications", [])
    awards = data.get("achievements", [])

    if not certs and not awards:
        return
    section_class = "pf-section-standalone" if standalone else "pf-section"
    cert_blocks = []
    local_pdf_certs = []
    for c in certs:
        link = c.get("link", "")
        local_path = None
        external_link_html = ""
        if link:
            if is_external_url(link):
                external_link_html = f' · <a href="{link}" target="_blank" class="pf-inline-link">View credential</a>'
            else:
                candidate = normalize_local_path(link)
                if asset_exists(candidate):
                    local_path = candidate

        cert_blocks.append(f"""
        <div class="pf-list-item pf-cert-item pf-reveal" data-has-buttons="{'1' if local_path else '0'}">
          <div class="pf-list-title">{c["name"]}</div>
          <div class="pf-list-meta">{c["issuer"]} · {c["year"]}{external_link_html}</div>
          <div class="pf-list-detail">{c["detail"]}</div>
        </div>
        """)
        if local_path:
            local_pdf_certs.append((c, local_path))

    award_blocks = "".join(f"""
    <div class="pf-list-item pf-reveal">
      <div class="pf-list-title">{a["title"]}</div>
      <div class="pf-list-meta">{a.get("year", "")}</div>
      <div class="pf-list-detail">{a["detail"]}</div>
    </div>
    """ for a in awards)

    certs_html = "".join(cert_blocks)
    awards_section = f"""
    <div class="pf-achievements-block">
      <div class="pf-eyebrow">Achievements</div>
      {award_blocks}
    </div>
    """ if awards else ""

    render_html(f"""
    <div id="achievements" class="{section_class} pf-wrap">
      <div class="pf-section-head">
        <div class="pf-eyebrow">07 — Recognition</div>
        <h2 class="pf-section-title">Certifications & achievements.</h2>
      </div>
      <div class="pf-eyebrow">Certifications</div>
      {certs_html}
      {awards_section}
    </div>
    """)
    for c, local_path in local_pdf_certs:
        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            pdf_view_button("View", local_path, c["name"], key=f"cert-view-{c['name']}", use_container_width=True)
        with col2:
            st.download_button(
                "Download",
                data=pdf_bytes(local_path),
                file_name=local_path.split("/")[-1],
                mime="application/pdf",
                key=f"cert-dl-{c['name']}",
                use_container_width=True,
            )
