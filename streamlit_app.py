# streamlit_app.py

import streamlit as st
from streamlit_option_menu import option_menu
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_chatbot
from dummy_tool2 import run as run_dummy2

st.set_page_config(page_title="CWCC AI-Tool App", layout="wide", initial_sidebar_state="expanded")

# ----------------------------------------------------------------------------
# Sidebar Navigation with option_menu
# ----------------------------------------------------------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Menue",
        options=["Home", "YouTube Quiz Generator", "AI Chatbot", "File Chat Tool"],
        icons=["house", "youtube", "robot", "file-earmark-text"],
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

    # Developer Footer
    st.markdown("---")
    st.markdown("**👨‍💻 Developer Info**", unsafe_allow_html=True)
    st.markdown(
        """
        Created by: Hilaria Li
        \nEmail: [lhn@cwcc.edu.hk](mailto:lhn@cwcc.edu.hk)  
        \nSchool: [Caritas Wu Cheng-chung College](https://www.cwcc.edu.hk/)  
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    # ----------------------------------------------------------------------------
    # 2) Social icons at the bottom of the sidebar
    # ----------------------------------------------------------------------------
    # (Replace the URLs below with your actual LinkedIn and GitHub profiles)
    linked_in_url = "https://www.linkedin.com/in/hilariali/"
    github_url = "https://github.com/trill01/"
    sidebar_footer = f"""
    <div style="position: absolute; bottom: 10px; width: 100%; text-align: center;">
      <a href="{linked_in_url}" target="_blank" style="margin-right: 12px;">
        <img src="https://cdn-icons-png.flaticon.com/24/174/174857.png" alt="LinkedIn" />
      </a>
      <a href="{github_url}" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/24/733/733553.png" alt="GitHub" />
      </a>
    </div>
    """
    st.markdown(sidebar_footer, unsafe_allow_html=True)

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
        """
    )
    st.write(
        """
        \n**Feedback Form**(https://forms.office.com/r/VLpSiCv5qP)
        \n**Wish Collection Form**(https://forms.office.com/r/DWBkQ91LL8)
        """
    )

elif selected == "YouTube Quiz Generator":
    run_youtube_quiz()

elif selected == "AI Chatbot":
    run_chatbot()

elif selected == "File Chat Tool":
    run_dummy2()
