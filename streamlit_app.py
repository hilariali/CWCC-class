import streamlit as st
from streamlit_option_menu import option_menu
from youtube_quiz import run as run_youtube_quiz
from dummy_tool1 import run as run_chatbot
from dummy_tool2 import run as run_dummy2
from website_summarizer import run as run_web_summarizer
from image_generator import run as run_image_generator
from text_to_speech import run as run_tts
from streamlit.components.v1 import html

# Translation dictionaries
TRANSLATIONS = {
    "en": {
        "app_title": "CWCC AI-Tool Hub",
        "menu_home": "Home",
        "menu_youtube": "YouTube Quiz Generator",
        "menu_chatbot": "AI Chatbot", 
        "menu_file": "File Chat Tool",
        "menu_web": "Web Summarizer",
        "menu_image": "Image Generator",
        "menu_tts": "Text to Speech",
        "home_title": "🏠 Home",
        "welcome_text": "Welcome to the CWCC AI-Tool Hub. Use the sidebar to switch between:",
        "youtube_desc": "Paste a YouTube URL, fetch captions, summarize, and create a quiz.",
        "chatbot_desc": "Chat with an AI powered by your secret API key.",
        "file_desc": "Upload documents and ask AI questions about them.",
        "web_desc": "Input a web URL, get the summary of webpage content.",
        "image_desc": "Create images from text prompts.",
        "tts_desc": "Convert text into spoken audio.",
        "learning_areas": "Learning Areas",
        "activity_approach": "Activity Approach",
        "feedback_form": "Feedback Form",
        "wish_form": "Wish Collection Form",
        "developer_info": "👨‍💻 Developer Info",
        "created_by": "Created by: Hilaria Li",
        "email": "Email:",
        "school": "School:"
    },
    "zh": {
        "app_title": "CWCC AI 工具中心",
        "menu_home": "首頁",
        "menu_youtube": "YouTube 測驗生成器",
        "menu_chatbot": "AI 聊天機器人",
        "menu_file": "文件對話工具",
        "menu_web": "網頁摘要器",
        "menu_image": "圖像生成器",
        "menu_tts": "文字轉語音",
        "home_title": "🏠 首頁",
        "welcome_text": "歡迎使用 CWCC AI 工具中心。使用側邊欄在以下工具間切換：",
        "youtube_desc": "貼上 YouTube 網址，擷取字幕，摘要並建立測驗。",
        "chatbot_desc": "使用您的密鑰與 AI 聊天。",
        "file_desc": "上傳文件並向 AI 提問相關問題。",
        "web_desc": "輸入網頁網址，獲取網頁內容摘要。",
        "image_desc": "從文字提示建立圖像。",
        "tts_desc": "將文字轉換為語音。",
        "learning_areas": "學習領域",
        "activity_approach": "活動方法",
        "feedback_form": "意見回饋表",
        "wish_form": "願望收集表",
        "developer_info": "👨‍💻 開發者資訊",
        "created_by": "開發者：李慧娜",
        "email": "電子郵件：",
        "school": "學校："
    }
}


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

def inject_custom_css():
    """Inject custom CSS for better contrast and layout"""
    st.markdown("""
    <style>
    /* Improve contrast for light mode */
    .stApp[data-theme="light"] {
        --primary-color: #1f77b4;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #262730;
        --border-color: #d6d6d6;
    }
    
    /* Improve contrast for dark mode */
    .stApp[data-theme="dark"] {
        --primary-color: #ff6b6b;
        --background-color: #0e1117;
        --secondary-background-color: #262730;
        --text-color: #fafafa;
        --border-color: #4a4a4a;
    }
    
    /* Ensure high contrast text */
    .stMarkdown, .stText, p, div, span {
        color: var(--text-color) !important;
    }
    
    /* Improve sidebar contrast */
    .css-1d391kg {
        background-color: var(--secondary-background-color) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Better button contrast */
    .stButton > button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border: 1px solid var(--primary-color) !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-color) !important;
        opacity: 0.8 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Improve form element contrast */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        border: 2px solid var(--border-color) !important;
    }
    
    /* Language switcher styling */
    .language-switcher {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 999;
        background: var(--secondary-background-color);
        padding: 5px 10px;
        border-radius: 5px;
        border: 1px solid var(--border-color);
    }
    
    /* Prevent text overflow */
    .stMarkdown, .stText {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
    }
    
    /* Ensure proper spacing */
    .main .block-container {
        padding: 1rem 1rem 10rem !important;
        max-width: 100% !important;
    }
    
    /* Fix sidebar text contrast */
    .css-1d391kg .stMarkdown, 
    .css-1d391kg p, 
    .css-1d391kg div {
        color: var(--text-color) !important;
    }
    
    /* Chinese font support */
    .chinese-text {
        font-family: "Microsoft YaHei", "PingFang TC", "Hiragino Sans GB", "Noto Sans CJK TC", "Source Han Sans TC", sans-serif !important;
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem 10rem !important;
        }
        
        .stButton > button {
            width: 100% !important;
            margin: 0.25rem 0 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def get_translation(key, lang="en"):
    """Get translation for a given key"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# Initialize session state for sidebar and language
if "sidebar_closed" not in st.session_state:
    st.session_state.sidebar_closed = False
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Home"
if "language" not in st.session_state:
    st.session_state.language = "en"

sidebar_state = "collapsed" if st.session_state.sidebar_closed else "expanded"

st.set_page_config(
    page_title="CWCC AI-Tool App",
    layout="wide",
    initial_sidebar_state=sidebar_state,
)

# Inject custom CSS for better contrast and layout
inject_custom_css()

# Language switcher in header
col1, col2 = st.columns([10, 1])
with col2:
    language_options = {"English": "en", "繁體中文": "zh"}
    selected_lang_display = st.selectbox(
        "🌐", 
        options=list(language_options.keys()),
        index=0 if st.session_state.language == "en" else 1,
        key="lang_selector"
    )
    if language_options[selected_lang_display] != st.session_state.language:
        st.session_state.language = language_options[selected_lang_display]
        st.rerun()

# ----------------------------------------------------------------------------
# Sidebar Navigation with option_menu
# ----------------------------------------------------------------------------
with st.sidebar:
    lang = st.session_state.language
    menu_items = [
        get_translation("menu_home", lang),
        get_translation("menu_youtube", lang),
        get_translation("menu_chatbot", lang),
        get_translation("menu_file", lang),
        get_translation("menu_web", lang),
        get_translation("menu_image", lang),
        get_translation("menu_tts", lang)
    ]
    
    selected = option_menu(
        menu_title="Menu",
        icons=["house", "youtube", "robot", "file-earmark-text", "globe", "image", "music-note-beamed"],
        options=menu_items,
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "transparent"},
            "icon": {"color": "#1f77b4", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "2px",
                "padding": "8px 12px",
                "--hover-color": "rgba(31, 119, 180, 0.1)",
                "color": "var(--text-color)",
                "border-radius": "5px",
            },
            "nav-link-selected": {
                "background-color": "rgba(31, 119, 180, 0.15)",
                "color": "var(--text-color)",
                "font-weight": "500",
                "border": "1px solid rgba(31, 119, 180, 0.3)"
            },
        },
    )

    # Map selected back to English for routing
    menu_mapping = {
        get_translation("menu_home", lang): "Home",
        get_translation("menu_youtube", lang): "YouTube Quiz Generator",
        get_translation("menu_chatbot", lang): "AI Chatbot",
        get_translation("menu_file", lang): "File Chat Tool",
        get_translation("menu_web", lang): "Web Summarizer",
        get_translation("menu_image", lang): "Image Generator",
        get_translation("menu_tts", lang): "Text to Speech"
    }
    
    selected_english = menu_mapping.get(selected, "Home")

    # If user selects a different menu, update state and rerun
    if selected_english != st.session_state.current_menu:
        st.session_state.current_menu = selected_english
        st.session_state.sidebar_closed = selected_english != "Home"
        st.rerun()

    # Developer Footer
    st.markdown("---")
    st.markdown(f"**{get_translation('developer_info', lang)}**", unsafe_allow_html=True)
    
    developer_text = f"""
        {get_translation('created_by', lang)}  
        {get_translation('email', lang)} [lhn@cwcc.edu.hk](mailto:lhn@cwcc.edu.hk)  
        {get_translation('school', lang)} [Caritas Wu Cheng-chung College](https://www.cwcc.edu.hk/)  
        """
    
    if lang == "zh":
        st.markdown(f'<div class="chinese-text">{developer_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(developer_text, unsafe_allow_html=True)
        
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
lang = st.session_state.language
main_title = get_translation("app_title", lang)

if lang == "zh":
    st.markdown(f'<h1 class="chinese-text">🔵🟡🔴 {main_title}</h1>', unsafe_allow_html=True)
else:
    st.title(f"🔵🟡🔴 {main_title}")

# ----------------------------------------------------------------------------
# Page Routing
# ----------------------------------------------------------------------------
if selected_english == "Home":
    home_title = get_translation("home_title", lang)
    if lang == "zh":
        st.markdown(f'<h2 class="chinese-text">{home_title}</h2>', unsafe_allow_html=True)
    else:
        st.header(home_title)
    
    welcome_text = get_translation("welcome_text", lang)
    
    if lang == "zh":
        # Format Chinese content properly
        content_html = f"""
        <div class="chinese-text">
            <p>{welcome_text}</p>
            <ul>
                <li><strong>{get_translation("menu_youtube", lang)}</strong>: {get_translation("youtube_desc", lang)}</li>
                <li><strong>{get_translation("menu_chatbot", lang)}</strong>: {get_translation("chatbot_desc", lang)}</li>
                <li><strong>{get_translation("menu_file", lang)}</strong>: {get_translation("file_desc", lang)}</li>
                <li><strong>{get_translation("menu_web", lang)}</strong>: {get_translation("web_desc", lang)}</li>
                <li><strong>{get_translation("menu_image", lang)}</strong>: {get_translation("image_desc", lang)}</li>
                <li><strong>{get_translation("menu_tts", lang)}</strong>: {get_translation("tts_desc", lang)}</li>
            </ul>
        </div>
        """
        st.markdown(content_html, unsafe_allow_html=True)
    else:
        content = f"""
            {welcome_text}

            - **{get_translation("menu_youtube", lang)}**: {get_translation("youtube_desc", lang)}
            - **{get_translation("menu_chatbot", lang)}**: {get_translation("chatbot_desc", lang)}
            - **{get_translation("menu_file", lang)}**: {get_translation("file_desc", lang)}
            - **{get_translation("menu_web", lang)}**: {get_translation("web_desc", lang)}
            - **{get_translation("menu_image", lang)}**: {get_translation("image_desc", lang)}
            - **{get_translation("menu_tts", lang)}**: {get_translation("tts_desc", lang)}
            """
        st.write(content)
        
    # Forms section
    if lang == "zh":
        feedback_html = f"""
        <div class="chinese-text">
            <p><strong>{get_translation("feedback_form", lang)}</strong>: <a href="https://forms.office.com/r/VLpSiCv5qP" target="_blank">https://forms.office.com/r/VLpSiCv5qP</a></p>
            <p><strong>{get_translation("wish_form", lang)}</strong>: <a href="https://forms.office.com/r/DWBkQ91LL8" target="_blank">https://forms.office.com/r/DWBkQ91LL8</a></p>
        </div>
        """
        st.markdown(feedback_html, unsafe_allow_html=True)
    else:
        feedback_text = f"""
        **{get_translation("feedback_form", lang)}**: [https://forms.office.com/r/VLpSiCv5qP](https://forms.office.com/r/VLpSiCv5qP)
        
        **{get_translation("wish_form", lang)}**: [https://forms.office.com/r/DWBkQ91LL8](https://forms.office.com/r/DWBkQ91LL8)
        """
        st.write(feedback_text)
        
elif selected_english == "YouTube Quiz Generator":
    run_youtube_quiz()
elif selected_english == "AI Chatbot":
    run_chatbot()
elif selected_english == "File Chat Tool":
    run_dummy2()
elif selected_english == "Web Summarizer":
    run_web_summarizer()
elif selected_english == "Image Generator":
    run_image_generator()
elif selected_english == "Text to Speech":
    run_tts()

# If collapsed state, collapse sidebar
if st.session_state.sidebar_closed:
    collapse_sidebar()
