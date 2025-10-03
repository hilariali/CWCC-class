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

def _add_dummy_info(resource):
    """Add dummy information to resources that lack detailed info"""
    dummy_descriptions = {
        "venue-booking-form": "Complete online form to reserve school facilities including auditorium, gymnasium, classrooms, and meeting rooms. Requires advance booking and approval.",
        "facility-report-form": "Report maintenance issues, safety concerns, or equipment malfunctions across campus facilities. Includes priority levels and tracking system.",
        "guest-parking-form": "Register visitor vehicles for campus access. Includes temporary parking permits and security clearance procedures.",
        "campus-floor-plan": "Interactive digital map showing building layouts, room numbers, emergency exits, and accessibility features across all campus facilities.",
        "staff-seating-plan": "Current seating arrangements for faculty and administrative staff. Updated regularly to reflect organizational changes.",
        "classroom-seating-chart": "Student seating arrangements by class and subject. Includes special accommodations and accessibility considerations.",
        "misbehaviour-form": "Disciplinary action form for student conduct issues. Covers uniform violations, behavioral incidents, and corrective measures.",
        "teacher-duty-list": "Weekly rotation schedule for teacher supervision duties including morning assembly, lunch periods, and after-school activities.",
        "morning-assembly": "Daily announcements, student recognition, and important school communications. Includes student ID card issue tracking.",
        "attendance-record": "Comprehensive student attendance tracking system with behavioral notes and parent communication logs.",
        "class-committee-list": "Student leadership positions and class representatives for the current academic term.",
        "credit-warning-form": "Academic performance tracking and intervention system. Requires form teacher consultation before submission.",
        "referral-form": "Student counseling and social work referral system for academic, behavioral, or personal support needs.",
        "class-building-materials": "Educational resources, supplies, and materials available for classroom activities and projects.",
        "gd-handbook": "Comprehensive guide covering school policies, disciplinary procedures, and student support services.",
        "conduct-evaluation": "Digital assessment system for student behavior and character development tracking.",
        "post-exam-activities": "Enrichment programs and activities scheduled during post-examination periods.",
        "ramadan-list": "Special scheduling and accommodations for Muslim students during the holy month of Ramadan.",
        "weekly-assembly": "Structured weekly gatherings for school announcements, presentations, and community building activities.",
        "class-teachers": "Directory of homeroom teachers with contact information and class assignments.",
        "canva-tool": "Professional design platform for creating educational materials, presentations, and visual content.",
        "filmora-tool": "Video editing software for creating educational content, presentations, and multimedia projects."
    }
    
    dummy_access_info = {
        "venue-booking-form": "Access through school portal → Facilities → Booking System. Requires staff login credentials and department approval.",
        "facility-report-form": "Available via maintenance portal or contact facilities management directly. Emergency issues: call ext. 2345.",
        "guest-parking-form": "Submit 24 hours in advance through security office. Include visitor details and purpose of visit.",
        "campus-floor-plan": "Available on school website → Campus Info → Interactive Map. Mobile app also available for download.",
        "staff-seating-plan": "Updated monthly on staff portal → Resources → Office Layout. Contact HR for changes or updates.",
        "classroom-seating-chart": "Access through teacher portal → Class Management → Seating Arrangements. Updated each semester.",
        "misbehaviour-form": "Available in teacher portal → Student Affairs → Disciplinary Forms. Requires supervisor approval.",
        "teacher-duty-list": "Posted weekly on staff bulletin board and teacher portal → Schedules → Duty Roster.",
        "morning-assembly": "Daily updates posted on school portal → Announcements. Student ID issues tracked in student affairs system.",
        "attendance-record": "Access through student information system → Attendance → Class Records. Real-time updates available.",
        "class-committee-list": "Updated each term on school portal → Student Life → Leadership. Elections held quarterly.",
        "credit-warning-form": "Available in academic portal → Student Progress → Intervention Forms. Requires form teacher consultation.",
        "referral-form": "Contact student counseling office directly or submit through student affairs portal → Support Services.",
        "class-building-materials": "Inventory available through supplies portal → Educational Resources. Request forms available online.",
        "gd-handbook": "Digital version available on school website → Student Resources → Policies. Print copies in main office.",
        "conduct-evaluation": "Access through student portal → Character Development → Assessment Tools. Updated system launching soon.",
        "post-exam-activities": "Schedule published on school calendar → Events → Academic Periods. Registration opens 2 weeks prior.",
        "ramadan-list": "Special schedules available through student affairs → Religious Accommodations. Updated annually.",
        "weekly-assembly": "Schedule and topics posted on school calendar → Events → Weekly Programs. Attendance mandatory.",
        "class-teachers": "Directory available on school portal → Staff → Faculty Contacts. Updated each semester.",
        "canva-tool": "Login credentials available from IT department. Training sessions offered monthly.",
        "filmora-tool": "Software installed on media lab computers. License details available from IT support."
    }
    
    # Add dummy info if missing
    if not resource.get("description") or len(resource.get("description", "").strip()) < 10:
        resource["description"] = dummy_descriptions.get(resource["id"], "Comprehensive resource providing essential tools and information for school operations and student services.")
    
    if not resource.get("placeholder_text") or len(resource.get("placeholder_text", "").strip()) < 20:
        resource["placeholder_text"] = dummy_access_info.get(resource["id"], "Access information and detailed instructions available through the school portal system. Contact administration for assistance.")
    
    return resource

def run(
    resources: Optional[List[Dict[str, Optional[str]]]] = None,
    app_base_url: Optional[str] = None,
    show_toc: bool = True,
    show_title: bool = True,
    title_text: str = "Resources Hub",
    subtitle_text: str = "Click on any resource title below to view detailed information"
):
    """Render the Resources Hub page with clean title list and top info card display."""
    data = resources if resources is not None else RESOURCES
    base = APP_BASE_URL if app_base_url is None else app_base_url

    # Initialize session state
    if "selected_resource" not in st.session_state:
        st.session_state.selected_resource = None

    # Prepare resources with dummy info
    processed = []
    for item in data:
        if not item or not item.get("title"):
            continue
        i = dict(item)
        i["anchor"] = _slugify(i["title"])
        i = _add_dummy_info(i)  # Add dummy info where needed
        processed.append(i)

    # *** SHOW THE TITLE FIRST ***
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

    # *** DISPLAY INFO CARD RIGHT AFTER TITLE ***
    if st.session_state.selected_resource:
        resource = st.session_state.selected_resource
        
        # Add scroll to top JavaScript
        st.markdown("""
        <script>
        setTimeout(function() {
            window.parent.document.querySelector('[data-testid="stAppViewContainer"]').scrollTop = 0;
        }, 100);
        </script>
        """, unsafe_allow_html=True)
        
        # Enhanced info card container with ID for targeting
        st.markdown("""
        <div id="info-card-container" style="background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%); 
                    padding: 30px; border-radius: 25px; margin: 25px 0; 
                    border: 3px solid #4a90e2; box-shadow: 0 20px 50px rgba(74, 144, 226, 0.2);
                    animation: slideDown 0.6s ease-out; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; 
                        background: linear-gradient(90deg, #4a90e2 0%, #667eea 50%, #764ba2 100%);"></div>
        </div>
        <style>
        @keyframes slideDown {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Enhanced header with close button
        col1, col2 = st.columns([9, 1])
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4a90e2 0%, #667eea 50%, #764ba2 100%); 
                        padding: 25px; border-radius: 18px; margin-bottom: 25px; 
                        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3); position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; 
                            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%); 
                            border-radius: 50%; transform: translate(20px, -20px);"></div>
                <h2 style="color: white; margin: 0; font-weight: 700; font-size: 28px; 
                           text-shadow: 0 2px 8px rgba(0,0,0,0.3); position: relative; z-index: 1;">
                    📋 {resource['title']}
                </h2>
                <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 14px; 
                          position: relative; z-index: 1;">
                    ✨ Resource Details - Click close (✖) to return to list
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            if st.button("✖ Close", key="close_info", help="Close info card and return to resource list"):
                st.session_state.selected_resource = None
                st.rerun()
        
        # Resource details
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Group info
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #1976d2; margin: 0 0 5px 0;">🏢 Department</h4>
                <p style="margin: 0; color: #424242;">{resource.get('group', 'General Resources')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Description
            desc = resource.get("description", "")
            if desc:
                st.markdown(f"""
                <div style="background: #fff8e1; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4 style="color: #f57c00; margin: 0 0 10px 0;">📝 Description</h4>
                    <p style="margin: 0; color: #424242; line-height: 1.6;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Access information
            access_info = resource.get("placeholder_text", "")
            if access_info:
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4 style="color: #388e3c; margin: 0 0 10px 0;">🔑 Access Information</h4>
                    <p style="margin: 0; color: #424242; line-height: 1.6;">{access_info}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("""
            <div style="background: #f3e5f5; padding: 15px; border-radius: 10px;">
                <h4 style="color: #7b1fa2; margin: 0 0 10px 0;">⚡ Quick Actions</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📞 Contact Support", key="contact_support", use_container_width=True):
                st.info("Contact information: admin@cwcc.edu.hk | Tel: +852 1234 5678")
            
            if st.button("📚 View Documentation", key="view_docs", use_container_width=True):
                st.info("Documentation will be available in the school portal system.")

        # Add extra spacing after info card
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        # Show helpful message when no resource is selected
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 20px; border-radius: 15px; margin: 20px 0; 
                    border: 2px dashed #dee2e6; text-align: center;">
            <h3 style="color: #6c757d; margin: 0 0 10px 0; font-weight: 600;">
                👇 Select a Resource Below
            </h3>
            <p style="color: #868e96; margin: 0; font-size: 14px;">
                Click on any resource title below to view detailed information right here
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar with grouped resources
    if show_toc:
        st.sidebar.header("📚 Resource Categories")
        by_group = {}
        for r in processed:
            grp = r.get("group", "Ungrouped")
            by_group.setdefault(grp, []).append(r)
        
        for group, items in by_group.items():
            with st.sidebar.expander(f"🏢 {group}", expanded=True):
                for r in items:
                    if st.sidebar.button(r['title'], key=f"sidebar_{r['anchor']}", use_container_width=True, help="Click to view details - will scroll to top"):
                        st.session_state.selected_resource = r
                        st.rerun()

    # Main content: Clean list of resources
    st.markdown("### 📋 Available Resources")
    st.markdown("*Click on any title to view detailed information*")
    
    # Group resources by category
    by_group = {}
    for r in processed:
        grp = r.get("group", "Ungrouped")
        by_group.setdefault(grp, []).append(r)
    
    # Display resources by group
    for group, items in by_group.items():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                    padding: 20px; border-radius: 15px; margin: 20px 0; 
                    border-left: 5px solid #667eea;">
            <h3 style="color: #2c3e50; margin: 0 0 15px 0;">🏢 {group}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display items in this group
        cols = st.columns(2)
        for idx, resource in enumerate(items):
            with cols[idx % 2]:
                # Clean title button with auto-scroll
                if st.button(
                    f"📄 {resource['title']}", 
                    key=f"main_{resource['anchor']}",
                    help=f"Click to view details about {resource['title']} - will scroll to top automatically",
                    use_container_width=True
                ):
                    st.session_state.selected_resource = resource
                    st.rerun()
                
                # Brief preview
                preview_text = resource.get('description', '')[:100]
                if len(preview_text) > 97:
                    preview_text = preview_text[:97] + "..."
                
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; 
                            margin-bottom: 15px; border-left: 3px solid #dee2e6;">
                    <small style="color: #6c757d; font-style: italic;">{preview_text}</small>
                </div>
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
        subtitle_text="Click on any resource title to view detailed information"
    )