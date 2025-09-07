import re
import streamlit as st

# Default dataset; you can pass your own via run(resources=...)
DEFAULT_RESOURCES = [
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

def _slugify(text: str) -> str:
    s = text.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9\\- ]", "", s)
    s = re.sub(r"\\s+", "-", s).strip("-")
    return s

def run_res (resources=None, app_base_url: str = "", show_toc: bool = True, show_title: bool = True):
    """
    Render the Resources page.

    Parameters
    ----------
    resources : list[dict] or None
        Items with keys: title, description, external_url, group.
        If None, uses DEFAULT_RESOURCES.
    app_base_url : str
        If set, titles will link to absolute URLs like {app_base_url}#anchor.
        Leave empty for relative #anchor links.
    show_toc : bool
        Show the sidebar Table of Contents.
    show_title : bool
        Show the top title "CWCC Resources Hub".
    """
    data = resources or DEFAULT_RESOURCES

    if show_title:
        st.title("CWCC Resources Hub")
        st.caption("Titles are deep-linkable to their sections. Form links are embedded in the text.")

    # Attach anchors
    for item in data:
        item["anchor"] = _slugify(item["title"])

    # Sidebar TOC
    if show_toc:
        st.sidebar.header("Jump to a Section")
        by_group = {}
        for r in data:
            by_group.setdefault(r["group"], []).append(r)
        for group, items in by_group.items():
            with st.sidebar.expander(group, expanded=True):
                for r in items:
                    link = f"{app_base_url}#{r['anchor']}" if app_base_url else f"#{r['anchor']}"
                    st.markdown(f"- [{r['title']}]({link})")

    st.markdown("---")

    # Sections
    for r in data:
        anchor = r["anchor"]
        # Invisible anchor
        st.markdown(f'<div id="{anchor}"></div>', unsafe_allow_html=True)

        # Title linked to its own section
        section_link = f"{app_base_url}#{anchor}" if app_base_url else f"#{anchor}"
        st.markdown(f"### [{r['title']}]({section_link})")

        # Embedded external/form link
        if r.get("description"):
            st.markdown(f"{r['description']} [Open the link]({r['external_url']}).")
        else:
            st.markdown(f"[Open the link here]({r['external_url']}).")

        st.divider()
