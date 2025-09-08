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
    subtitle_text: str = "Click on section titles to view detailed information. Resources will be accessible through the directory system."
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

    # Initialize session state for popup
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False
    if "popup_resource" not in st.session_state:
        st.session_state.popup_resource = None

    # Prepare anchors
    processed = []
    for item in data:
        if not item or not item.get("title"):
            continue
        i = dict(item)
        i["anchor"] = _slugify(i["title"])
        processed.append(i)

    # Sidebar TOC with popup functionality
    if show_toc:
        st.sidebar.header("Resource Sections")
        by_group = {}
        for r in processed:
            grp = r.get("group", "Ungrouped")
            by_group.setdefault(grp, []).append(r)
        for group, items in by_group.items():
            with st.sidebar.expander(group, expanded=True):
                for r in items:
                    # Create clickable button for each resource in sidebar
                    if st.sidebar.button(f"📋 {r['title']}", key=f"sidebar_{r['anchor']}", help="Click to view details"):
                        st.session_state.show_popup = True
                        st.session_state.popup_resource = r

    st.markdown("---")

    # Sections with clickable headers
    cols = st.columns([1, 1, 1])  # Create a 3-column layout for better organization
    col_idx = 0
    
    for r in processed:
        anchor = r["anchor"]
        # Invisible anchor for deep linking
        st.markdown(f'<div id="{anchor}"></div>', unsafe_allow_html=True)
        
        with cols[col_idx % 3]:
            # Create a card-like container for each resource with enhanced styling
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 2px solid #e3f2fd; 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 15px 5px; 
                    background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    cursor: pointer;
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        margin-bottom: 10px;
                    ">
                        <div style="
                            width: 40px;
                            height: 40px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            margin-right: 15px;
                        ">
                            <span style="color: white; font-size: 18px;">📋</span>
                        </div>
                        <h4 style="margin: 0; color: #1565c0; font-weight: 600;">{r['title']}</h4>
                    </div>
                    <div style="
                        background: rgba(255,255,255,0.8);
                        padding: 8px 12px;
                        border-radius: 20px;
                        margin-bottom: 15px;
                        display: inline-block;
                    ">
                        <small style="color: #666; font-weight: 500;">
                            🏢 {r.get('group', 'Ungrouped')}
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced clickable button with better styling
                st.markdown("""
                <style>
                .stButton > button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 14px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                    transition: all 0.3s ease;
                    width: 100%;
                }
                .stButton > button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }
                </style>
                """, unsafe_allow_html=True)
                
                if st.button(
                    f"🔍 View Details", 
                    key=f"main_{anchor}", 
                    help=f"Click to view details about {r['title']}",
                    use_container_width=True
                ):
                    st.session_state.show_popup = True
                    st.session_state.popup_resource = r
        
        col_idx += 1

    # Display popup modal
    if st.session_state.show_popup and st.session_state.popup_resource:
        # Add JavaScript for smooth scrolling to popup
        st.markdown("""
        <script>
        setTimeout(function() {
            const popup = document.querySelector('[data-testid="stMarkdownContainer"]:has-text("📋 Resource Details")');
            if (popup) {
                popup.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 100);
        </script>
        """, unsafe_allow_html=True)
        
        with st.container():
            # Create prominent modal-like overlay with enhanced styling
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin: 20px 0;
                border: 3px solid #4CAF50;
            ">
                <h2 style="color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                    📋 Resource Details
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            resource = st.session_state.popup_resource
            
            # Enhanced layout with better visual hierarchy
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 5px solid #007bff;
                    margin: 10px 0;
                ">
                    <h2 style="color: #007bff; margin: 0;">{resource['title']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("✖ Close", key="close_popup", help="Close resource details"):
                    st.session_state.show_popup = False
                    st.session_state.popup_resource = None
                    st.rerun()
            
            # Enhanced information display with better styling
            st.markdown(f"""
            <div style="
                background: #e3f2fd;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border: 1px solid #bbdefb;
            ">
                <strong style="color: #1976d2;">Group:</strong> {resource.get('group', 'Ungrouped')}
            </div>
            """, unsafe_allow_html=True)
            
            desc = (resource.get("description") or "").strip()
            placeholder = (resource.get("placeholder_text") or "").strip()
            
            if desc:
                st.markdown("**Description:**")
                st.markdown(f"""
                <div style="
                    background: #fff3e0;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    border-left: 4px solid #ff9800;
                ">
                    {desc}
                </div>
                """, unsafe_allow_html=True)
            
            if placeholder:
                st.markdown("**Access Information:**")
                st.info(f"📍 {placeholder}")
            
            # Technical information
            resource_id = resource.get("id", "")
            page_function = resource.get("page_function", "")
            if resource_id or page_function:
                with st.expander("🔧 Technical Information", expanded=False):
                    if resource_id:
                        st.code(f"Resource ID: {resource_id}")
                    if page_function:
                        st.code(f"Page Function: {page_function}")
            
            # Deep link with enhanced styling
            section_link = f"{base}#{resource['anchor']}" if base else f"#{resource['anchor']}"
            st.markdown(f"""
            <div style="
                background: #e8f5e8;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border: 1px solid #4caf50;
                text-align: center;
            ">
                <strong>Direct Link:</strong> 
                <a href="{section_link}" style="
                    color: #2e7d32;
                    text-decoration: none;
                    font-weight: bold;
                    background: #4caf50;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    margin-left: 10px;
                ">🔗 {resource['title']}</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a prominent separator
            st.markdown("""
            <div style="
                height: 4px;
                background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
                border-radius: 2px;
                margin: 20px 0;
            "></div>
            """, unsafe_allow_html=True)

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
