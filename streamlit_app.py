import streamlit as st
from streamlit_option_menu import option_menu
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_chatbot
from dummy_tool2 import run as run_dummy2
from website_summarizer import run as run_web_summarizer
from image_generator import run as run_image_generator
from text_to_speech import run as run_tts
from streamlit.components.v1 import html
from auth import check_authentication, authenticate_user, logout
from resource import run as run_res
# Set page config first
st.set_page_config(
    page_title="CWCC AI-Tool App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Authentication check - if not authenticated, show login page
if not check_authentication():
    authenticate_user()
    st.stop()  # Stop execution here if not authenticated

# If we reach here, user is authenticated - show the main app

def collapse_sidebar():
    """Trigger sidebar collapse via JavaScript."""
    html(
        """
        <script>
        const btn = window.parent.document.querySelector('button[title="Collapse sidebar"], button[data-testid="collapse-control"]');
        if (btn) { btn.click(); }
        </script>
        """,
        height=0,
    )

# Initialize session state for sidebar
if "sidebar_closed" not in st.session_state:
    st.session_state.sidebar_closed = False
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Home"

sidebar_state = "collapsed" if st.session_state.sidebar_closed else "expanded"

# ----------------------------------------------------------------------------
# Sidebar Navigation with option_menu
# ----------------------------------------------------------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        icons=["house", "youtube", "robot", "file-earmark-text", "globe", "image", "music-note-beamed", "globe"],
        options=["Home", "YouTube Quiz Generator", "AI Chatbot", "File Chat Tool", "Web Summarizer", "Image Generator", "Text to Speech", "Resources"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "blue", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "2px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#d0e6ff"},
        },
    )

    # If user selects a different menu, update state and rerun
    if selected != st.session_state.current_menu:
        st.session_state.current_menu = selected
        st.session_state.sidebar_closed = selected != "Home"
        st.rerun()

    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()

    # Developer Footer
    st.markdown("---")
    st.markdown("**👨‍💻 Developer Info**", unsafe_allow_html=True)
    st.markdown(
        """
        Created by: Hilaria Li  
        Email: [lhn@cwcc.edu.hk](mailto:lhn@cwcc.edu.hk)  
        School: [Caritas Wu Cheng-chung College](https://www.cwcc.edu.hk/)  
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    linked_in_url = "https://www.linkedin.com/in/hilariali/"
    github_url = "https://github.com/hilariali/"
    st.markdown(
        f"""
        <div style='position:absolute; bottom:10px; width:100%; text-align:center;'>
          <a href='{linked_in_url}' target='_blank' style='margin-right:12px;'>
            <img src='https://cdn-icons-png.flaticon.com/24/174/174857.png' alt='LinkedIn'/>
          </a>
          <a href='{github_url}' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/24/733/733553.png' alt='GitHub'/>
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Main Page Header
# ----------------------------------------------------------------------------
st.title("🔵🟡🔴 CWCC AI-Tool Hub")

# ----------------------------------------------------------------------------
# Page Routing
# ----------------------------------------------------------------------------
if selected == "Home":
    st.header("🏠 Home")
    st.write(
        """
        Welcome to the CWCC AI-Tool Hub. Use the sidebar to switch between:

        - **YouTube Quiz Generator**: Paste a YouTube URL, fetch captions, summarize, and create a quiz.
        - **AI Chatbot**: Chat with an AI powered by your secret API key.
        - **File Chat Tool**: Upload documents and ask AI questions about them.
        - **Web Summarizer**: Input a web URL, get the summary of webpage content.
        - **Image Generator**: Create images from text prompts.
        - **Text to Speech**: Convert text into spoken audio.
        """
    )
    st.write(
        """
        
        **Feedback Form**(https://forms.office.com/r/VLpSiCv5qP)
        
        **Wish Collection Form**(https://forms.office.com/r/DWBkQ91LL8)
        """
    )
elif selected == "YouTube Quiz Generator":
    run_youtube_quiz()
elif selected == "AI Chatbot":
    run_chatbot()
elif selected == "File Chat Tool":
    run_dummy2()
elif selected == "Web Summarizer":
    run_web_summarizer()
elif selected == "Image Generator":
    run_image_generator()
elif selected == "Text to Speech":
    run_tts()
elif selected == "Resources":
    run_res()

# If collapsed state, collapse sidebar
if st.session_state.sidebar_closed:
    collapse_sidebar()
