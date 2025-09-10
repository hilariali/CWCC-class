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
    {"id": "venue-booking-form", "title": "Venue Booking Form", "description": "For booking school venues (TKN/Tiana).", "placeholder_text": "Please contact the office to access the venue booking form.", "group": "School Innovation Development"},
    {"id": "facility-report-form", "title": "Abnormalities in Campus Facilities Report Form", "description": "Report campus facility issues (Anson/Yan).", "placeholder_text": "Please contact the facility management to report issues.", "group": "School Innovation Development"},
    {"id": "guest-parking-form", "title": "Guest Car Parking Registration Form", "description": "Register guest vehicles (Tiana/Yan).", "placeholder_text": "Please contact security to register guest vehicles.", "group": "School Innovation Development"},
    {"id": "campus-floor-plan", "title": "Floor Plan of Campus", "description": "Google Sheet containing the campus layout.", "placeholder_text": "Campus floor plan will be available through the directory system.", "group": "School Innovation Development"},
    {"id": "staff-seating-plan", "title": "Staff Room Seating Plan", "description": "Staff seating arrangements.", "placeholder_text": "Staff seating arrangements will be available through the directory system.", "group": "School Innovation Development"},
    {"id": "classroom-seating-chart", "title": "Classroom Seating Chart", "description": "Classroom seating charts.", "placeholder_text": "Classroom seating charts will be available through the directory system.", "group": "School Innovation Development"},

    # --- 2526 Student Innovation Development (from Word) ---
    {"id": "misbehaviour-form", "title": "Misbehaviour Form", "description": "Card & uniform ONLY.", "placeholder_text": "Please contact student affairs to access the misbehaviour form.", "page_function": "misbehaviour_form", "group": "Student Innovation Development"},
    {"id": "teacher-duty-list", "title": "Teacher On-duty List (教師當值)", "description": "Schedules (1/9–4/9 and from 5/9 onwards).", "placeholder_text": "Teacher duty schedules will be available through the directory system.", "page_function": "teacher_duty", "group": "Student Innovation Development"},
    {"id": "morning-assembly", "title": "Morning Assembly – Announcement / Card Issue (早會宣佈/學生証)", "description": "CT must check daily.", "placeholder_text": "Morning assembly announcements will be available through the directory system.", "page_function": "morning_assembly", "group": "Student Innovation Development"},
    {"id": "attendance-record", "title": "Attendance & Behavioural Record / Sunshine Call", "description": "", "placeholder_text": "Attendance and behavioural records will be available through the directory system.", "page_function": "attendance_record", "group": "Student Innovation Development"},
    {"id": "class-committee-list", "title": "Class Committee List (1st Term)", "description": "", "placeholder_text": "Class committee information will be available through the directory system.", "page_function": "class_committee", "group": "Student Innovation Development"},
    {"id": "credit-warning-form", "title": "Credit/Warning Form", "description": "Please discuss with Form Teacher first.", "placeholder_text": "Please contact your form teacher to access the credit/warning form.", "page_function": "credit_warning", "group": "Student Innovation Development"},
    {"id": "referral-form", "title": "Referral Form", "description": "Refer to social worker.", "placeholder_text": "Please contact student counseling services for referral forms.", "page_function": "referral_form", "group": "Student Innovation Development"},
    {"id": "class-building-materials", "title": "Class Building Materials", "description": "", "placeholder_text": "Class building materials will be available through the directory system.", "page_function": "class_materials", "group": "Student Innovation Development"},
    {"id": "gd-handbook", "title": "G & D Handbook", "description": "", "placeholder_text": "Guidance and Discipline handbook will be available through the directory system.", "page_function": "gd_handbook", "group": "Student Innovation Development"},
    {"id": "conduct-evaluation", "title": "e-Conduct Evaluation (To be updated)", "description": "", "placeholder_text": "Conduct evaluation system will be available through the directory system.", "page_function": "conduct_eval", "group": "Student Innovation Development"},
    {"id": "post-exam-activities", "title": "Post Exam Activities (To be updated)", "description": "", "placeholder_text": "Post exam activities information will be available through the directory system.", "page_function": "post_exam", "group": "Student Innovation Development"},
    {"id": "ramadan-list", "title": "Ramadan List (To be updated)", "description": "", "placeholder_text": "Ramadan schedule information will be available through the directory system.", "page_function": "ramadan_list", "group": "Student Innovation Development"},
    {"id": "weekly-assembly", "title": "Weekly Assembly (2526 週會節)", "description": "", "placeholder_text": "Weekly assembly information will be available through the directory system.", "page_function": "weekly_assembly", "group": "Student Innovation Development"},
    {"id": "class-teachers", "title": "Class Teachers", "description": "", "placeholder_text": "Class teacher information will be available through the directory system.", "page_function": "class_teachers", "group": "Student Innovation Development"},

    # --- Additional Tools ---
    {"id": "canva-tool", "title": "Canva", "description": "Design resources login — Email: designcwcc@cwcc.edu.hk / Password: CWCCstandas1#", "placeholder_text": "Canva design tool access will be available through the directory system.", "page_function": "canva_tool", "group": "Additional Tools"},
    {"id": "filmora-tool", "title": "Filmora (Wondershare)", "description": "Video editing software — Email: designcwcc@cwcc.edu.hk / Password: CWCCstandas1#", "placeholder_text": "Filmora video editing software access will be available through the directory system.", "page_function": "filmora_tool", "group": "Additional Tools"},
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

def _add_scroll_to_popup_js():
    """Add JavaScript to automatically scroll to popup when it appears"""
    return """
    <script>
    function scrollToPopup() {
        setTimeout(function() {
            // Look for the popup container
            const popupElements = window.parent.document.querySelectorAll('[data-testid="stMarkdown"]');
            let popupFound = false;
            
            for (let element of popupElements) {
                if (element.innerHTML.includes('📋 Resource Details')) {
                    element.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start',
                        inline: 'nearest'
                    });
                    popupFound = true;
                    break;
                }
            }
            
            // Alternative method - scroll to bottom if popup not found via content
            if (!popupFound) {
                const containers = window.parent.document.querySelectorAll('[data-testid="stVerticalBlock"]');
                if (containers.length > 0) {
                    const lastContainer = containers[containers.length - 1];
                    lastContainer.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }
            }
        }, 200);
    }
    
    // Execute scroll function
    scrollToPopup();
    
    // Also execute on any state changes
    setTimeout(scrollToPopup, 500);
    setTimeout(scrollToPopup, 1000);
    </script>
    """

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
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 20px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        ">
            <h1 style="
                color: white;
                margin: 0;
                font-weight: 700;
                font-size: 36px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            ">{title_text}</h1>
            {f'<p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">{subtitle_text}</p>' if subtitle_text else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Add custom CSS for better button styling
        st.markdown("""
        <style>
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
            background: linear-gradient(135deg, #5a6fd8 0%, #6b5b95 100%);
        }
        .stButton > button:active {
            transform: translateY(0);
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state for popup
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False
    if "popup_resource" not in st.session_state:
        st.session_state.popup_resource = None
    if "should_scroll" not in st.session_state:
        st.session_state.should_scroll = False

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
                        st.session_state.should_scroll = True
                        st.rerun()

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
                # Clickable title area that triggers popup
                title_clicked = st.button(
                    f"📋 {r['title']}", 
                    key=f"title_{anchor}",
                    help=f"Click to view details about {r['title']}",
                    use_container_width=True
                )
                
                if title_clicked:
                    st.session_state.show_popup = True
                    st.session_state.popup_resource = r
                    st.session_state.should_scroll = True
                    st.rerun()
                
                # Enhanced card design with proper markdown
                card_html = f"""
                <div style="border: 2px solid #e3f2fd; border-radius: 15px; padding: 15px; margin: 10px 5px; background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%); box-shadow: 0 6px 20px rgba(0,0,0,0.08); transition: all 0.3s ease; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);"></div>
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 8px 12px; border-radius: 20px; margin-bottom: 12px; display: inline-block; border: 1px solid rgba(102, 126, 234, 0.2);">
                        <small style="color: #4c6ef5; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">🏢 {r.get('group', 'Ungrouped')}</small>
                    </div>
                    <div style="color: #495057; font-size: 13px; line-height: 1.4; margin-top: 8px;">
                        {(r.get('description', 'Click to view more details') or 'Click to view more details')[:80]}{'...' if len(r.get('description', '')) > 80 else ''}
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Add a small hint that the card is clickable
                hint_html = """
                <div style="text-align: center; margin-top: 8px; padding: 6px; background: rgba(102, 126, 234, 0.05); border-radius: 8px; border: 1px dashed rgba(102, 126, 234, 0.3);">
                    <small style="color: #6c757d; font-style: italic; font-size: 11px;">💡 Click title above for details</small>
                </div>
                """
                st.markdown(hint_html, unsafe_allow_html=True)
        
        col_idx += 1

    # Display popup modal
    if st.session_state.show_popup and st.session_state.popup_resource:
        # Add auto-scroll JavaScript when popup should be shown
        if st.session_state.should_scroll:
            st.markdown(_add_scroll_to_popup_js(), unsafe_allow_html=True)
            st.session_state.should_scroll = False  # Reset scroll flag
        
        with st.container():
            # Add unique ID for targeting the popup
            popup_header_html = """
            <div id="resource-popup-container" style="background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%); padding: 25px; border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.1); margin: 25px 0; border: 2px solid #e3f2fd; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #4ecdc4 100%);"></div>
                <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                        <span style="color: white; font-size: 24px;">📋</span>
                    </div>
                    <h2 style="color: #2c3e50; margin: 0; font-weight: 700; font-size: 28px; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">Resource Details</h2>
                </div>
            </div>
            """
            st.markdown(popup_header_html, unsafe_allow_html=True)
            
            resource = st.session_state.popup_resource
            
            # Enhanced layout with better visual hierarchy
            col1, col2, col3 = st.columns([5, 1, 1])
            with col1:
                header_html = f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin: 10px 0; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
                    <h2 style="color: white; margin: 0; font-weight: 700; font-size: 24px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">🏷️ {resource['title']}</h2>
                </div>
                """
                st.markdown(header_html, unsafe_allow_html=True)
            
            with col3:
                if st.button("✖ Close", key="close_popup", help="Close resource details"):
                    st.session_state.show_popup = False
                    st.session_state.popup_resource = None
                    st.session_state.should_scroll = False
                    st.rerun()
            
            # Enhanced information display with better styling  
            group_html = f"""
            <div style="background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%); padding: 18px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #667eea; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 18px; margin-right: 8px;">🏢</span>
                    <strong style="color: #495057; font-size: 16px;">Group:</strong>
                </div>
                <div style="background: rgba(102, 126, 234, 0.1); padding: 8px 15px; border-radius: 20px; display: inline-block; border: 1px solid rgba(102, 126, 234, 0.2);">
                    <span style="color: #4c6ef5; font-weight: 600; font-size: 14px;">{resource.get('group', 'Ungrouped')}</span>
                </div>
            </div>
            """
            st.markdown(group_html, unsafe_allow_html=True)
            
            desc = (resource.get("description") or "").strip()
            placeholder = (resource.get("placeholder_text") or "").strip()
            
            if desc:
                desc_html = f"""
                <div style="background: linear-gradient(135deg, #fff8e1 0%, #ffffff 100%); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #ffa726; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 20px; margin-right: 10px;">📝</span>
                        <h3 style="color: #e65100; margin: 0; font-weight: 600; font-size: 18px;">Description</h3>
                    </div>
                    <div style="color: #424242; font-size: 15px; line-height: 1.6; background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 8px; border: 1px solid rgba(255, 167, 38, 0.2);">
                        {desc}
                    </div>
                </div>
                """
                st.markdown(desc_html, unsafe_allow_html=True)
            
            if placeholder:
                placeholder_html = f"""
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%); padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #4caf50; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 20px; margin-right: 10px;">🔑</span>
                        <h3 style="color: #2e7d32; margin: 0; font-weight: 600; font-size: 18px;">Access Information</h3>
                    </div>
                    <div style="background: rgba(76, 175, 80, 0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(76, 175, 80, 0.3); color: #2e7d32; font-size: 15px; line-height: 1.5; display: flex; align-items: center;">
                        <span style="font-size: 18px; margin-right: 10px;">📍</span>
                        {placeholder}
                    </div>
                </div>
                """
                st.markdown(placeholder_html, unsafe_allow_html=True)
            
            # Technical information with enhanced styling
            resource_id = resource.get("id", "")
            page_function = resource.get("page_function", "")
            if resource_id or page_function:
                with st.expander("🔧 Technical Information", expanded=False):
                    tech_html = """
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    """
                    st.markdown(tech_html, unsafe_allow_html=True)
                    if resource_id:
                        st.code(f"Resource ID: {resource_id}", language="text")
                    if page_function:
                        st.code(f"Page Function: {page_function}", language="text")
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Enhanced direct link section
            section_link = f"{base}#{resource['anchor']}" if base else f"#{resource['anchor']}"
            link_html = f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%); padding: 20px; border-radius: 12px; margin: 20px 0; border: 2px solid #2196f3; text-align: center; box-shadow: 0 6px 20px rgba(33, 150, 243, 0.2);">
                <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                    <span style="font-size: 20px; margin-right: 10px;">🔗</span>
                    <h3 style="color: #1976d2; margin: 0; font-weight: 600;">Direct Link</h3>
                </div>
                <a href="{section_link}" style="color: white; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); padding: 12px 24px; border-radius: 25px; display: inline-block; margin-top: 10px; box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(33, 150, 243, 0.6)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(33, 150, 243, 0.4)'">
                    🚀 Go to {resource['title']}
                </a>
            </div>
            """
            st.markdown(link_html, unsafe_allow_html=True)
            
            # Add a prominent separator
            separator_html = """
            <div style="height: 4px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57); border-radius: 2px; margin: 20px 0;"></div>
            """
            st.markdown(separator_html, unsafe_allow_html=True)

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
