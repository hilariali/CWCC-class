# streamlit_app.py
import streamlit as st

# Import each tool’s “run” function
from youtube_quiz import run_quiz_generator
from dummy_tool1 import run_dummy_tool1
from dummy_tool2 import run_dummy_tool2

# ──────────────────────────────────────────────────────────────────────────────
# Main page configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Multi‐Tool Hub", layout="wide")
st.sidebar.title("🔧 Tools Menu")

# Sidebar navigation
page = st.sidebar.radio(
    "Go to:",
    ("Home", "YouTube Quiz Generator", "Dummy Tool 1", "Dummy Tool 2"),
)

# ──────────────────────────────────────────────────────────────────────────────
# Landing / Router
# ──────────────────────────────────────────────────────────────────────────────
if page == "Home":
    st.title("Welcome to the Multi‐Tool Hub 🚀")
    st.markdown(
        """
        **Select one of the tools from the left sidebar:**
        
        1. **YouTube Quiz Generator** – Paste a YouTube URL, fetch/transcribe, summarize with OpenAI, and generate a multiple‐choice quiz.  
        2. **Dummy Tool 1** – This is just a placeholder that demonstrates how to wire up a second tool.  
        3. **Dummy Tool 2** – Another placeholder (different UI) to show that you can add as many as you like.  
        
        Feel free to switch pages via the sidebar above. Each tool is isolated in its own module.  
        """
    )

elif page == "YouTube Quiz Generator":
    run_quiz_generator()

elif page == "Dummy Tool 1":
    run_dummy_tool1()

elif page == "Dummy Tool 2":
    run_dummy_tool2()
