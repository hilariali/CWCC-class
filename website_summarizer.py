import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import traceback

client = None

CHUNK_SIZE = 100000

def fetch_page_text(url: str) -> str:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(separator="\n")
    except Exception:
        return ""

def summarize_chunk(text: str, lang: str) -> str:
    prompt = f"Please summarize the following webpage text in {lang}:\n\n{text}"
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

def summarize_text(text: str, lang: str) -> str:
    if len(text) <= CHUNK_SIZE:
        return summarize_chunk(text, lang)
    parts = []
    for i in range(0, len(text), CHUNK_SIZE):
        parts.append(summarize_chunk(text[i : i + CHUNK_SIZE], lang))
    return summarize_chunk("\n".join(parts), lang)

def run():
    global client
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )

    st.header("\U0001F310 Webpage Summarizer")
    url = st.text_input("Website URL:")
    lang = st.text_input("Language for summary:", value="English")

    if st.button("Summarize"):
        if not url.strip():
            st.warning("Please enter a URL.")
            return
        with st.spinner("Fetching webpage…"):
            text = fetch_page_text(url.strip())
        if not text:
            st.error("Failed to fetch or parse the webpage.")
            return
        with st.spinner("Summarizing…"):
            summary = summarize_text(text, lang.strip() or "English")
        if summary:
            st.subheader("Summary")
            st.write(summary)
