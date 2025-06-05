# streamlit_app.py

import streamlit as st
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_dummy1
from dummy_tool2 import run as run_dummy2

st.set_page_config(page_title="Multi‐Tool App", layout="wide")
st.title("📋 Multi‐Tool Streamlit Hub")

st.write(
    """
    Welcome! From this landing page, choose one of the tools below:
    - **YouTube Quiz Generator**: Given a YouTube URL, fetch captions, summarize, and build a multiple-choice quiz.
    - **Dummy Tool 1**: Placeholder tool.
    - **Dummy Tool 2**: Another placeholder.
    """
)

choice = st.selectbox(
    "Select a tool:",
    [
        "— Home (this page) —",
        "YouTube Quiz Generator",
        "Dummy Tool 1",
        "Dummy Tool 2",
    ],
)

if choice == "YouTube Quiz Generator":
    run_youtube_quiz()
elif choice == "Dummy Tool 1":
    run_dummy1()
elif choice == "Dummy Tool 2":
    run_dummy2()
else:
    st.info("Use the dropdown above to pick a tool.")
