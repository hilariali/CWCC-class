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
    {"id": "venue-booking-form", "title": "Venue Booking Form", "description": "For booking school venues (TKN/Tiana).", "placeholder_text": "Please contact the office to access the venue booking form.", "page_function": "venue_booking", "group": "School Innovation Development"},
    {"id": "facility-report-form", "title": "Abnormalities in Campus Facilities Report Form", "description": "Report campus facility issues (Anson/Yan).", "placeholder_text": "Please contact the facilities team to report any campus issues.", "page_function": "facility_report", "group": "School Innovation Development"},
    {"id": "guest-parking-form", "title": "Guest Car Parking Registration Form", "description": "Register guest vehicles (Tiana/Yan).", "placeholder_text": "Please contact security to register guest vehicles.", "page_function": "guest_parking", "group": "School Innovation Development"},
    {"id": "campus-floor-plan", "title": "Floor Plan of Campus", "description": "Google Sheet containing the campus layout.", "placeholder_text": "Campus floor plan will be available through the directory system.", "page_function": "campus_layout", "group": "School Innovation Development"},
    {"id": "staff-seating-plan", "title": "Staff Room Seating Plan", "description": "Staff seating arrangements.", "placeholder_text": "Staff seating arrangements will be available through the directory system.", "page_function": "staff_seating", "group": "School Innovation Development"},
    {"id": "classroom-seating-chart", "title": "Classroom Seating Chart", "description": "Classroom seating charts.", "placeholder_text": "Classroom seating charts will be available through the directory system.", "page_function": "classroom_seating", "group": "School Innovation Development"},

    # --- 2526 Student Innovation Development (from Word) ---
    {"id": "misbehaviour-form", "title": "Misbehaviour Form", "description": "Card & uniform ONLY.", "placeholder_text": "Please contact student affairs to access the misbehaviour form.", "page_function": "misbehaviour_form", "group": "2526 Student Innovation Development"},
    {"id": "teacher-duty-list", "title": "Teacher On-duty List (教師當值)", "description": "Schedules (1/9–4/9 and from 5/9 onwards).", "placeholder_text": "Teacher duty schedules will be available through the directory system.", "page_function": "teacher_duty", "group": "2526 Student Innovation Development"},
    {"id": "morning-assembly", "title": "Morning Assembly – Announcement / Card Issue (早會宣佈/學生証)", "description": "CT must check daily.", "placeholder_text": "Morning assembly announcements will be available through the directory system.", "page_function": "morning_assembly", "group": "2526 Student Innovation Development"},
    {"id": "attendance-record", "title": "Attendance & Behavioural Record / Sunshine Call", "description": "", "placeholder_text": "Attendance and behavioural records will be available through the directory system.", "page_function": "attendance_record", "group": "2526 Student Innovation Development"},
    {"id": "class-committee-list", "title": "Class Committee List (1st Term)", "description": "", "placeholder_text": "Class committee information will be available through the directory system.", "page_function": "class_committee", "group": "2526 Student Innovation Development"},
    {"id": "credit-warning-form", "title": "Credit/Warning Form", "description": "Please discuss with Form Teacher first.", "placeholder_text": "Please contact your form teacher to access the credit/warning form.", "page_function": "credit_warning", "group": "2526 Student Innovation Development"},
    {"id": "referral-form", "title": "Referral Form", "description": "Refer to social worker.", "placeholder_text": "Please contact student counseling services for referral forms.", "page_function": "referral_form", "group": "2526 Student Innovation Development"},
    {"id": "class-building-materials", "title": "Class Building Materials", "description": "", "placeholder_text": "Class building materials will be available through the directory system.", "page_function": "class_materials", "group": "2526 Student Innovation Development"},
    {"id": "gd-handbook", "title": "G & D Handbook", "description": "", "placeholder_text": "Guidance and Discipline handbook will be available through the directory system.", "page_function": "gd_handbook", "group": "2526 Student Innovation Development"},
    {"id": "conduct-evaluation", "title": "e-Conduct Evaluation (To be updated)", "description": "", "placeholder_text": "Conduct evaluation system will be available through the directory system.", "page_function": "conduct_evaluation", "group": "2526 Student Innovation Development"},
    {"id": "post-exam-activities", "title": "Post Exam Activities (To be updated)", "description": "", "placeholder_text": "Post exam activities information will be available through the directory system.", "page_function": "post_exam_activities", "group": "2526 Student Innovation Development"},
    {"id": "ramadan-list", "title": "Ramadan List (To be updated)", "description": "", "placeholder_text": "Ramadan schedule information will be available through the directory system.", "page_function": "ramadan_list", "group": "2526 Student Innovation Development"},
    {"id": "weekly-assembly", "title": "Weekly Assembly (2526 週會節)", "description": "", "placeholder_text": "Weekly assembly information will be available through the directory system.", "page_function": "weekly_assembly", "group": "2526 Student Innovation Development"},
    {"id": "class-teachers", "title": "Class Teachers", "description": "", "placeholder_text": "Class teacher information will be available through the directory system.", "page_function": "class_teachers", "group": "2526 Student Innovation Development"},

    # --- Additional Tools ---
    {"id": "canva-tool", "title": "Canva", "description": "Design resources login — Email: designcwcc@cwcc.edu.hk / Password: CWCCstandas1#", "placeholder_text": "Canva design tool access will be available through the directory system.", "page_function": "canva_tool", "group": "Additional Tools"},
    {"id": "filmora-tool", "title": "Filmora (Wondershare)", "description": "Video editing software — Email: designcwcc@cwcc.edu.hk / Password: CWCCstandas1#", "placeholder_text": "Filmora video editing tool access will be available through the directory system.", "page_function": "filmora_tool", "group": "Additional Tools"},
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
    subtitle_text: str = "Titles deep-link to sections. Resources will be accessible through the directory system."
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

        # Display description and placeholder text
        desc = (r.get("description") or "").strip()
        placeholder = (r.get("placeholder_text") or "").strip()
        
        if desc and placeholder:
            st.markdown(f"{desc}")
            st.info(f"📍 {placeholder}")
        elif desc and not placeholder:
            st.markdown(desc)
        elif placeholder and not desc:
            st.info(f"📍 {placeholder}")
        
        # Display resource ID and page function for reference
        resource_id = r.get("id", "")
        page_function = r.get("page_function", "")
        if resource_id or page_function:
            with st.expander("🔧 Technical Info", expanded=False):
                if resource_id:
                    st.code(f"Resource ID: {resource_id}")
                if page_function:
                    st.code(f"Page Function: {page_function}")

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
        subtitle_text="Titles deep-link to sections. Resources will be accessible through the directory system."
    )
