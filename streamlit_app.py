# streamlit_app.py

import streamlit as st
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_chatbot
from dummy_tool2 import run as run_dummy2

st.set_page_config(page_title="Multi‐Tool App", layout="wide", initial_sidebar_state="expanded")

# ----------------------------------------------------------------------------
# 1) Sidebar Navigation (toggleable by user)
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Go to:",
        ["Home", "YouTube Quiz Generator", "AI Chatbot", "Dummy Tool 2"],
        index=0,
    )

# ----------------------------------------------------------------------------
# 2) Dispatch to selected page
# ----------------------------------------------------------------------------
st.title("📋 Multi‐Tool Streamlit Hub")

if page == "Home":
    st.header("🏠 Home")
    st.write(
        """
        Welcome to the Multi‐Tool Streamlit App! Use the sidebar to switch between:

        - **YouTube Quiz Generator**: Paste a YouTube URL, fetch captions, summarize, and create a quiz.
        - **AI Chatbot**: Chat with an AI powered by your secret API key.
        - **Dummy Tool 2**: A placeholder/demo.
        """
    )

elif page == "YouTube Quiz Generator":
    run_youtube_quiz()

elif page == "AI Chatbot":
    run_chatbot()

elif page == "Dummy Tool 2":
    run_dummy2()
