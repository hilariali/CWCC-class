# youtube_quiz.py

import streamlit as st
import re
import openai
import traceback
import requests
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

client = None
CHUNK_SIZE = 100000

def get_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url.strip()

def parse_proxies(proxy_input: str) -> list[str]:
    return [u.strip() for u in proxy_input.split(",") if u.strip()]

def list_languages_yt_dlp(video_id: str) -> dict:
    try:
        ydl_opts = {"skip_download": True, "quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            langs: dict[str, str] = {}
            subs = info.get("subtitles") or {}
            for code in subs.keys():
                langs[code] = "manual"
            auto = info.get("automatic_captions") or {}
            for code in auto.keys():
                if code not in langs:
                    langs[code] = "auto"
            return langs
    except Exception:
        return {}

def try_list_transcripts_api(video_id: str, proxies: dict | None) -> dict:
    try:
        ts_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
        return {t.language_code: ("auto" if t.is_generated else "manual") for t in ts_list}
    except (TranscriptsDisabled, NoTranscriptFound, Exception):
        return {}

def list_transcript_languages(video_id: str, proxy_list: list[str]) -> tuple[dict, dict | None]:
    st.info("Attempting to list languages via yt_dlp…")
    langs = list_languages_yt_dlp(video_id)
    if langs:
        st.success(f"✓ Languages found via yt_dlp: {', '.join(langs.keys())}")
        return langs, None
    st.info("Falling back to YouTubeTranscriptApi (no proxy)…")
    langs = try_list_transcripts_api(video_id, None)
    if langs:
        st.success("✓ Languages found via API without proxy")
        return langs, None
    for p in proxy_list:
        proxy_cfg = {"http": p, "https": p}
        st.info(f"Trying proxy {p} for YouTubeTranscriptApi…")
        langs = try_list_transcripts_api(video_id, proxy_cfg)
        if langs:
            st.success(f"✓ Languages found via API proxy {p}")
            return langs, proxy_cfg
    st.error("✗ Unable to list transcript languages (yt_dlp + API all failed)")
    return {}, None

def fetch_transcript_yt_dlp(video_id: str, lang: str) -> str:
    try:
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "subtitleslangs": [lang],
            "subtitlesformat": "vtt",
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            subs = info.get("subtitles") or {}
            if lang in subs:
                vtt_url = subs[lang][0].get("url")
            else:
                auto = info.get("automatic_captions") or {}
                if lang in auto:
                    vtt_url = auto[lang][0].get("url")
                else:
                    return ""
            r = requests.get(vtt_url, timeout=10)
            vtt_text = r.text
            lines = []
            for row in vtt_text.splitlines():
                if row.startswith("WEBVTT") or re.match(r"^\d\d:\d\d:\d\d\.\d\d\d -->", row):
                    continue
                lines.append(row)
            return "\n".join(lines).strip()
    except Exception:
        return ""

def try_fetch_transcript_api(video_id: str, lang: str, proxies: dict | None) -> str:
    try:
        entries = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang], proxies=proxies)
        return "\n".join(e.get("text", "") for e in entries)
    except (TranscriptsDisabled, NoTranscriptFound, Exception):
        return ""

def fetch_transcript_with_fallback(video_id: str, lang: str, proxy_list: list[str]) -> tuple[str, dict | None]:
    st.info("Attempting to fetch transcript via yt_dlp…")
    text = fetch_transcript_yt_dlp(video_id, lang)
    if text:
        st.success("✓ Fetched transcript via yt_dlp")
        return text, None
    st.info("Falling back to YouTubeTranscriptApi (no proxy)…")
    text = try_fetch_transcript_api(video_id, lang, None)
    if text:
        st.success("✓ Fetched transcript via API without proxy")
        return text, None
    for p in proxy_list:
        proxy_cfg = {"http": p, "https": p}
        st.info(f"Trying proxy {p} for YouTubeTranscriptApi…")
        text = try_fetch_transcript_api(video_id, lang, proxy_cfg)
        if text:
            st.success(f"✓ Fetched transcript via API proxy {p}")
            return text, proxy_cfg
    st.error("✗ Unable to fetch transcript (yt_dlp + API all failed)")
    return "", None

def summarize_chunk(text: str, lang: str) -> str:
    prompt = f"Please summarize the following transcript chunk in {lang}:\n\n{text}"
    try:
        resp = client.chat.completions.create(
            model="Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"Summarization error: {e}")
        st.text(traceback.format_exc())
        return ""

def summarize_transcript(transcript: str, lang: str) -> str:
    if len(transcript) <= CHUNK_SIZE:
        return summarize_chunk(transcript, lang)
    parts = []
    for i in range(0, len(transcript), CHUNK_SIZE):
        parts.append(summarize_chunk(transcript[i : i + CHUNK_SIZE], lang))
    return summarize_chunk("\n".join(parts), lang)

def generate_quiz(summary: str, lang: str, grade: str, num_questions: int) -> str:
    prompt = (
        f"Create a {num_questions}-question multiple-choice quiz in {lang} "
        f"for grade {grade} students based on this summary:\n\n{summary}"
    )
    try:
        resp = client.chat.completions.create(
            model="Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"Quiz generation error: {e}")
        st.text(traceback.format_exc())
        return ""

def modify_quiz(existing_quiz: str, instructions: str, lang: str) -> str:
    prompt = (
        f"Modify this quiz in {lang} as follows: {instructions}\n\n"
        f"Current quiz:\n{existing_quiz}"
    )
    try:
        resp = client.chat.completions.create(
            model="Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"Quiz modification error: {e}")
        st.text(traceback.format_exc())
        return ""

def run():
    global client
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )
    
    # Get language from session state if available
    lang = getattr(st.session_state, 'language', 'en')
    
    # Translation dictionary for YouTube Quiz Generator
    translations = {
        "en": {
            "title": "📚 YouTube Quiz Generator",
            "caption": "*(Beta: only works on videos with captions)*",
            "url_label": "YouTube video URL:",
            "proxy_label": "Optional: HTTP(S) proxy URLs (comma-separated):",
            "load_button": "Load Video & Proxies",
            "lang_select": "Transcript language:",
            "show_transcript": "Show Transcript",
            "transcript_title": "🔹 Transcript",
            "transcript_label": "Transcript text:",
            "summary_button": "Generate Summary",
            "summary_title": "🔹 Summary",
            "grade_label": "Student's grade level:",
            "num_questions": "Number of questions:",
            "quiz_button": "Generate Quiz",
            "quiz_title": "🔹 Quiz",
            "modify_label": "Modification instructions:",
            "modify_button": "Modify Quiz",
        },
        "zh": {
            "title": "📚 YouTube 測驗生成器",
            "caption": "*(測試版：僅適用於有字幕的影片)*",
            "url_label": "YouTube 影片網址：",
            "proxy_label": "可選：HTTP(S) 代理伺服器網址（逗號分隔）：",
            "load_button": "載入影片和代理伺服器",
            "lang_select": "字幕語言：",
            "show_transcript": "顯示字幕",
            "transcript_title": "🔹 字幕內容",
            "transcript_label": "字幕文字：",
            "summary_button": "生成摘要",
            "summary_title": "🔹 摘要",
            "grade_label": "學生年級：",
            "num_questions": "問題數量：",
            "quiz_button": "生成測驗",
            "quiz_title": "🔹 測驗",
            "modify_label": "修改說明：",
            "modify_button": "修改測驗",
        }
    }
    
    def get_text(key):
        return translations.get(lang, translations["en"]).get(key, key)

    defaults = {
        "last_url": "",
        "proxies": "",
        "submitted": False,
        "video_id": "",
        "langs": {},
        "used_proxy_for_langs": None,
        "selected_lang": "",
        "transcript": "",
        "used_proxy_for_transcript": None,
        "transcript_fetched": False,
        "summary": "",
        "summary_generated": False,
        "quiz": "",
        "quiz_generated": False,
        "mod_instructions": "",
        "updated_quiz": "",
        "updated_pending": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Display title and caption with translation
    if lang == "zh":
        st.markdown(f'<h2 class="chinese-text">{get_text("title")}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="chinese-text"><em>{get_text("caption")}</em></p>', unsafe_allow_html=True)
    else:
        st.header(get_text("title"))
        st.caption(get_text("caption"))

    with st.form(key="input_form", clear_on_submit=False):
        url_label = get_text("url_label")
        proxy_label = get_text("proxy_label")
        load_button_text = get_text("load_button")
        
        if lang == "zh":
            st.markdown(f'<p class="chinese-text">{url_label}</p>', unsafe_allow_html=True)
            url_input = st.text_input("", value=st.session_state.last_url, label_visibility="collapsed", key="url_input_zh")
            st.markdown(f'<p class="chinese-text">{proxy_label}</p>', unsafe_allow_html=True)
            proxy_input = st.text_input("", value=st.session_state.proxies, label_visibility="collapsed", key="proxy_input_zh")
        else:
            url_input = st.text_input(url_label, value=st.session_state.last_url, key="url_input_en")
            proxy_input = st.text_input(proxy_label, value=st.session_state.proxies, key="proxy_input_en")
        
        submit_button = st.form_submit_button(label=load_button_text)

    if submit_button:
        st.session_state.last_url = url_input.strip()
        st.session_state.proxies = proxy_input.strip()
        st.session_state.submitted = True
        st.session_state.video_id = get_video_id(st.session_state.last_url)
        st.session_state.langs = {}
        st.session_state.used_proxy_for_langs = None
        st.session_state.selected_lang = ""
        st.session_state.transcript = ""
        st.session_state.used_proxy_for_transcript = None
        st.session_state.transcript_fetched = False
        st.session_state.summary = ""
        st.session_state.summary_generated = False
        st.session_state.quiz = ""
        st.session_state.quiz_generated = False
        st.session_state.mod_instructions = ""
        st.session_state.updated_quiz = ""
        st.session_state.updated_pending = False

    if st.session_state.submitted and st.session_state.last_url:
        vid = st.session_state.video_id
        proxy_list = parse_proxies(st.session_state.proxies)

        if not st.session_state.langs:
            langs, used_proxy = list_transcript_languages(vid, proxy_list)
            st.session_state.langs = langs
            st.session_state.used_proxy_for_langs = used_proxy

        if not st.session_state.langs:
            st.error("No transcripts available—yt_dlp & API both failed, or IP blocked.")
        else:
            lang_select_label = get_text("lang_select")
            if lang == "zh":
                st.markdown(f'<p class="chinese-text">{lang_select_label}</p>', unsafe_allow_html=True)
            st.session_state.selected_lang = st.selectbox(
                "" if lang == "zh" else lang_select_label, 
                list(st.session_state.langs.keys()), 
                index=0,
                label_visibility="collapsed" if lang == "zh" else "visible"
            )

            if not st.session_state.transcript_fetched:
                if st.button(get_text("show_transcript")):
                    text, used_proxy_trans = fetch_transcript_with_fallback(
                        vid,
                        st.session_state.selected_lang,
                        proxy_list,
                    )
                    st.session_state.transcript = text
                    st.session_state.used_proxy_for_transcript = used_proxy_trans
                    if not text:
                        st.error("Failed to fetch transcript—yt_dlp & API both failed.")
                    else:
                        st.session_state.transcript_fetched = True

            if st.session_state.transcript_fetched and st.session_state.transcript:
                st.subheader("🔹 Transcript")
                st.text_area(
                    "Transcript text:",
                    value=st.session_state.transcript,
                    height=200,
                    disabled=True,
                )

                if not st.session_state.summary_generated:
                    if st.button("Generate Summary"):
                        with st.spinner("Summarizing transcript…"):
                            st.session_state.summary = summarize_transcript(
                                st.session_state.transcript,
                                st.session_state.selected_lang,
                            )
                            st.session_state.summary_generated = True

            if st.session_state.summary_generated and st.session_state.summary:
                st.subheader("🔹 Summary")
                st.write(st.session_state.summary)

                grade = st.text_input("Student's grade level:", value="10")
                num_q = st.number_input(
                    "Number of questions:", min_value=1, max_value=20, value=5
                )
                if not st.session_state.quiz_generated:
                    if st.button("Generate Quiz"):
                        with st.spinner("Creating quiz…"):
                            st.session_state.quiz = generate_quiz(
                                st.session_state.summary,
                                st.session_state.selected_lang,
                                grade,
                                int(num_q),
                            )
                            st.session_state.quiz_generated = True

            if st.session_state.quiz_generated and st.session_state.quiz:
                st.subheader("🔹 Quiz")
                st.write(st.session_state.quiz)

                st.markdown("**Modify the quiz (optional):**")
                _ = st.text_area(
                    "Enter modification instructions:",
                    value=st.session_state.mod_instructions,
                    key="mod_instructions",
                    height=120,
                )

                if st.button("Apply Modifications"):
                    instructions = st.session_state.mod_instructions
                    if instructions.strip():
                        with st.spinner("Applying modifications…"):
                            modified = modify_quiz(
                                st.session_state.quiz,
                                instructions,
                                st.session_state.selected_lang,
                            )
                            if modified:
                                st.session_state.updated_quiz = modified
                                st.session_state.updated_pending = True
                                st.success("Modifications ready. Click 'Show Updated Quiz' to view.")
                    else:
                        st.warning("Please enter instructions to modify the quiz.")

                if st.session_state.updated_pending:
                    if st.button("Show Updated Quiz"):
                        st.session_state.quiz = st.session_state.updated_quiz
                        st.session_state.updated_pending = False
                        st.success("Displaying updated quiz below.")
                        st.subheader("🔹 Quiz (Updated)")
                        st.write(st.session_state.quiz)
