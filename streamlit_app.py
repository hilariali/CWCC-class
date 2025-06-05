# streamlit_app.py

import streamlit as st
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_dummy1
from dummy_tool2 import run as run_dummy2

st.set_page_config(page_title="Multi-Tool Web App", layout="wide")


# ------------------------------------------------------------
# 1) Define a small helper to render the top “nav bar”
# ------------------------------------------------------------
def render_navbar(current_page: str):
    """
    Renders a simple horizontal nav bar with links that set ?page=… 
    """
    # Define all pages and their titles
    PAGES = {
        "home": "🏠 Home",
        "youtube_quiz": "📚 YouTube Quiz Generator",
        "dummy1": "🔧 Dummy Tool 1",
        "dummy2": "🛠 Dummy Tool 2",
    }

    # Minimal CSS to space out links and highlight the active one
    st.markdown(
        """
        <style>
        .nav-link {
            margin-right: 20px;
            font-size: 18px;
            text-decoration: none;
            color: #0366d6;
        }
        .nav-link-active {
            font-weight: bold;
            color: #000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Build the clickable links (no target="_blank", so open in the same tab)
    link_md = []
    for key, title in PAGES.items():
        if key == current_page:
            link_md.append(
                f"<a class='nav-link-active' href='?page={key}'>{title}</a>"
            )
        else:
            link_md.append(f"<a class='nav-link' href='?page={key}'>{title}</a>")

    st.markdown("  |  ".join(link_md), unsafe_allow_html=True)
    st.markdown("---")  # horizontal rule to separate navbar from content


# ------------------------------------------------------------
# 2) Detect which “page” we’re on via query params
# ------------------------------------------------------------
query_params = st.query_params
current_page = query_params.get("page", ["home"])[0]

# Sanity-check “current_page” against our known pages
valid_pages = {"home", "youtube_quiz", "dummy1", "dummy2"}
if current_page not in valid_pages:
    current_page = "home"

# ------------------------------------------------------------
# 3) Render nav bar at top
# ------------------------------------------------------------
render_navbar(current_page)

# ------------------------------------------------------------
# 4) Dispatch to the appropriate “run()” for that page
# ------------------------------------------------------------
if current_page == "home":
    st.title("🎉 Welcome to the Multi-Tool Web App")
    st.write(
        """
        This is the landing page. Use the navigation bar above to jump to any tool:

        - **Home (🏠)**: This page.
        - **YouTube Quiz Generator (📚)**: Paste a YouTube URL and generate a quiz from its captions.
        - **Dummy Tool 1 (🔧)**: A placeholder/demo page.
        - **Dummy Tool 2 (🛠)**: Another placeholder/demo page.
        """
    )
    st.write("Simply click on one of the links in the nav bar to get started!")

elif current_page == "youtube_quiz":
    # Call into youtube_quiz.py’s run() 
    run_youtube_quiz()

elif current_page == "dummy1":
    run_dummy1()

elif current_page == "dummy2":
    run_dummy2()
