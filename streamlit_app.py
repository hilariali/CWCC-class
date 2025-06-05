# streamlit_app.py

import streamlit as st
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_dummy1
from dummy_tool2 import run as run_dummy2

st.set_page_config(page_title="Multi-Tool Web App", layout="wide")


# ------------------------------------------------------------
# 1) Define a helper to render the top “nav bar” using buttons
# ------------------------------------------------------------
def render_navbar(current_page: str):
    """
    Renders a simple horizontal nav bar with buttons that update ?page=…
    in the same tab (via st.experimental_set_query_params).
    """
    PAGES = {
        "home": "🏠 Home",
        "youtube_quiz": "📚 YouTube Quiz Generator",
        "dummy1": "🔧 Dummy Tool 1",
        "dummy2": "🛠 Dummy Tool 2",
    }

    cols = st.columns(len(PAGES))
    for idx, (key, title) in enumerate(PAGES.items()):
        if key == current_page:
            # Highlight the active page (render as bold text)
            cols[idx].markdown(f"**{title}**")
        else:
            # Render a button for each non-active page
            if cols[idx].button(title, key=f"nav_btn_{key}"):
                st.experimental_set_query_params(page=key)
                # Once we set the new query param, immediately return so Streamlit will rerun
                return

    st.markdown("---")  # horizontal rule under the nav bar


# ------------------------------------------------------------
# 2) Detect which “page” we’re on via experimental_get_query_params
# ------------------------------------------------------------
query_params = st.experimental_get_query_params()
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
    st.write("Simply click one of the buttons in the nav bar to get started!")

elif current_page == "youtube_quiz":
    run_youtube_quiz()

elif current_page == "dummy1":
    run_dummy1()

elif current_page == "dummy2":
    run_dummy2()
