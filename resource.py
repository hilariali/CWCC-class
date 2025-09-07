import re
import streamlit as st
from typing import List, Dict, Optional

# Handle secrets gracefully - only access when in Streamlit context
try:
    APP_BASE_URL = st.secrets.get("APP_BASE_URL", "")
except:
    APP_BASE_URL = ""  # leave empty for relative links; set to absolute base URL if deployed

# ---------------------------
# Resource Data (All in one file)
# ---------------------------
RESOURCES: List[Dict[str, Optional[str]]] = [
    # --- School Innovation Development (from PDF) ---
    {"title": "Venue Booking Form", "description": "For booking school venues (TKN/Tiana).", "external_url": "https://forms.gle/N8SAHGRRBibBjJy78", "group": "School Innovation Development"},
    {"title": "Abnormalities in Campus Facilities Report Form", "description": "Report campus facility issues (Anson/Yan).", "external_url": "https://forms.gle/D6vE49j7VatquoLm6", "group": "School Innovation Development"},
    {"title": "Guest Car Parking Registration Form", "description": "Register guest vehicles (Tiana/Yan).", "external_url": "https://forms.gle/DRc6PVSbjsq2bHGx6", "group": "School Innovation Development"},
    {"title": "Floor Plan of Campus", "description": "Google Sheet containing the campus layout.", "external_url": "https://docs.google.com/spreadsheets/d/1XNOQR8vhxlXj2zpVwNtSaZ_ntq10yDI37FXkwD4O8As/edit?usp=sharing", "group": "School Innovation Development"},
    {"title": "Staff Room Seating Plan", "description": "Staff seating arrangements.", "external_url": "https://docs.google.com/spreadsheets/d/1hnBIBlmQqBjQC8qUqX_LCXhuk9LP42mvMRNCbzaSJ8g/edit?usp=sharing", "group": "School Innovation Development"},
    {"title": "Classroom Seating Chart", "description": "Classroom seating charts.", "external_url": "https://docs.google.com/spreadsheets/d/1DJbamFd5gNmEqBe-zlWODBoqdU_lCPXdA_3Ymrw58Ro/edit?usp=sharing", "group": "School Innovation Development"},

    # --- 2526 Student Innovation Development (from Word) ---
    {"title": "Misbehaviour Form", "description": "Card & uniform ONLY.", "external_url": "https://forms.gle/VDPiL1CFQLYmdSff7", "group": "2526 Student Innovation Development"},
    {"title": "Teacher On-duty List (教師當值)", "description": "Schedules (1/9–4/9 and from 5/9 onwards).", "external_url": "https://forms.gle/XM7WQAyuSXmQhPFn6", "group": "2526 Student Innovation Development"},
    {"title": "Morning Assembly – Announcement / Card Issue (早會宣佈/學生証)", "description": "CT must check daily.", "external_url": "https://drive.google.com/drive/folders/1QQxMRJ2O3EtW_TAgKvI3l1JQYsaerJow?usp=drive_link", "group": "2526 Student Innovation Development"},
    {"title": "Attendance & Behavioural Record / Sunshine Call", "description": "", "external_url": "https://docs.google.com/document/d/1mgayREPsgpRqJsC3eHodWjn-DVDSOPhxjkA1d3TIGWE/edit?usp=drive_link", "group": "2526 Student Innovation Development"},
    {"title": "Class Committee List (1st Term)", "description": "", "external_url": "https://docs.google.com/spreadsheets/d/1NDaW7YXF_vDj05Os0AWLSK8vdg63-ptYE6hWl2sf4KQ/edit?usp=sharing", "group": "2526 Student Innovation Development"},
    {"title": "Credit/Warning Form", "description": "Please discuss with Form Teacher first.", "external_url": "https://forms.gle/TMaRvDsAM8K8S2B5A", "group": "2526 Student Innovation Development"},
    {"title": "Referral Form", "description": "Refer to social worker.", "external_url": "https://drive.google.com/file/d/1b4-Uwz2fclhOHQaIPKIVbfViRv-K19ls/view?usp=drive_link", "group": "2526 Student Innovation Development"},
    {"title": "Class Building Materials", "description": "", "external_url": "https://docs.google.com/document/d/1I79w_6ldXjjO62_QO-cyCEMU24IPbDO9S_IXtcZZ8fA/edit?tab=t.0", "group": "2526 Student Innovation Development"},
    {"title": "G & D Handbook", "description": "", "external_url": "https://drive.google.com/file/d/1SrUon3n-eGl8Uz7yLMLp8dYDQev1aYck/view?usp=drive_link", "group": "2526 Student Innovation Development"},
    {"title": "e-Conduct Evaluation (To be updated)", "description": "", "external_url": "https://docs.google.com/spreadsheets/d/193Hhysj5NhMEeSqJsOXN7mfXX_8AxZO_4J0I31Q-wrI/edit#gid=684919084", "group": "2526 Student Innovation Development"},
    {"title": "Post Exam Activities (To be updated)", "description": "", "external_url": "https://docs.google.com/spreadsheets/d/193Hhysj5NhMEeSqJsOXN7mfXX_8AxZO_4J0I31Q-wrI/edit#gid=684919084", "group": "2526 Student Innovation Development"},
    {"title": "Ramadan List (To be updated)", "description": "", "external_url": "https://docs.google.com/spreadsheets/d/193Hhysj5NhMEeSqJsOXN7mfXX_8AxZO_4J0I31Q-wrI/edit#gid=684919084", "group": "2526 Student Innovation Development"},
    {"title": "Weekly Assembly (2526 週會節)", "description": "", "external_url": "https://docs.google.com/document/d/1w-7vyZ2vfuEjRvYvbhRd7v-CSHGZxFSmaukaJhf_XZc/edit?tab=t.0", "group": "2526 Student Innovation Development"},
    {"title": "Class Teachers", "description": "", "external_url": "https://docs.google.com/spreadsheets/d/1TCgRVvk1J55bzxcqLHaMvAhnBB8BKOo405MOFJTQibI/edit?gid=1506328782#gid=1506328782", "group": "2526 Student Innovation Development"},

    # --- Additional Tools ---
    {"title": "Canva", "description": "Design resources login — Email: designcwcc@cwcc.edu.hk / Password: CWCCstandas1#", "external_url": "https://www.canva.com/", "group": "Additional Tools"},
    {"title": "Filmora (Wondershare)", "description": "Video editing software — Email: designcwcc@cwcc.edu.hk / Password: CWCCstandas1#", "external_url": "https://filmora.wondershare.com/video-editor/", "group": "Additional Tools"},
]

# ---------------------------
# Utilities
# ---------------------------
def _slugify(text: str) -> str:
    s = text.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s

def run(
    resources: Optional[List[Dict[str, Optional[str]]]] = None,
    app_base_url: Optional[str] = None,
    show_toc: bool = True,
    show_title: bool = True,
    title_text: str = "Resources Hub",
    subtitle_text: str = "Titles deep-link to sections. External links are embedded in the text."
):
    """Render the Resources Hub page.

    If `resources` is None, uses the built-in RESOURCES list in this file.
    If `app_base_url` is None, uses APP_BASE_URL from secrets (or "").
    """
    data = resources if resources is not None else RESOURCES
    base = APP_BASE_URL if app_base_url is None else app_base_url

    if show_title:
        st.title(title_text)
        if subtitle_text:
            st.caption(subtitle_text)

    # Prepare anchors
    processed = []
    for item in data:
        if not item or not item.get("title"):
            continue
        i = dict(item)
        i["anchor"] = _slugify(i["title"])
        processed.append(i)

    # Sidebar TOC
    if show_toc:
        st.sidebar.header("Jump to a Section")
        by_group = {}
        for r in processed:
            grp = r.get("group", "Ungrouped")
            by_group.setdefault(grp, []).append(r)
        for group, items in by_group.items():
            with st.sidebar.expander(group, expanded=True):
                for r in items:
                    link = f"{base}#{r['anchor']}" if base else f"#{r['anchor']}"
                    st.markdown(f"- [{r['title']}]({link})")

    st.markdown("---")

    # Sections
    for r in processed:
        anchor = r["anchor"]
        # Invisible anchor
        st.markdown(f'<div id="{anchor}"></div>', unsafe_allow_html=True)

        # Title linked to its own deep link
        section_link = f"{base}#{anchor}" if base else f"#{anchor}"
        st.markdown(f"### [{r['title']}]({section_link})")

        # Embedded external link in the text (if provided)
        desc = (r.get("description") or "").strip()
        url = (r.get("external_url") or "").strip()
        if desc and url:
            st.markdown(f"{desc} [Open the link]({url}).")
        elif desc and not url:
            st.markdown(desc)
        elif url and not desc:
            st.markdown(f"[Open the link here]({url}).")

        st.divider()

# Standalone execution
if __name__ == "__main__":
    st.set_page_config(page_title="Resources Hub", page_icon="🔗", layout="wide")
    run(
        resources=None,  # use built-in data above
        app_base_url=None,  # use APP_BASE_URL secret (or default "")
        show_toc=True,
        show_title=True,
        title_text="CWCC Resources Hub",
        subtitle_text="Titles deep-link to sections. External links are embedded in the text."
    )
