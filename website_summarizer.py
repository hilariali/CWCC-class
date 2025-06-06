import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import traceback

client = None

MAX_CONTEXT = 100000



CHUNK_SIZE = 100000

def fetch_page_text(url: str) -> str:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(separator="\n")
    except Exception:
        return ""

def summarize_chunk(text: str) -> str:
    prompt = (
        "Please summarize the following webpage text in the same language as "
        f"the text:\n\n{text}"
    )
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

def summarize_text(text: str) -> str:
    if len(text) <= CHUNK_SIZE:
        return summarize_chunk(text)
    parts = []
    for i in range(0, len(text), CHUNK_SIZE):
        parts.append(summarize_chunk(text[i : i + CHUNK_SIZE]))
    return summarize_chunk("\n".join(parts))

def run():
    global client
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )

    st.header("\U0001F310 Webpage Summarizer")
    url = st.text_input("Website URL:")


    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

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
            summary = summarize_text(text)
        if summary:

            st.session_state.page_text = text
            st.session_state.summary = summary
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "Hi! Ask me questions about this webpage.",
                }
            ]
            st.subheader("Summary")
            st.write(st.session_state.summary)

    if "summary" in st.session_state:
        st.subheader("Chat About the Page")
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "Hi! Ask me questions about this webpage.",
                }
            ]

        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

        user_input = st.chat_input("Your question about the page…")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            system_prompt = (
                "You are an assistant answering questions based solely on the provided webpage text. "
                "If the answer is not contained in the text or you are uncertain, say you do not know and suggest verifying."
            )
            context = st.session_state.page_text[:MAX_CONTEXT]
            messages = [{"role": "system", "content": system_prompt + "\n\n" + context}] + st.session_state.chat_history

            with st.spinner("Thinking…"):
                try:
                    resp = client.chat.completions.create(
                        model="Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=messages,
                    )
                    reply = resp.choices[0].message.content
                except Exception as e:
                    reply = f"Error: {e}"

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)

            st.subheader("Summary")
            st.write(st.session_state.summary)

