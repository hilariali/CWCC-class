# dummy_tool2.py

import streamlit as st
import openai
from io import BytesIO
from docx import Document
from pptx import Presentation
import PyPDF2

def extract_text_from_file(file, file_type):
    if file_type == "txt":
        return file.read().decode("utf-8")

    elif file_type == "pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in reader.pages])

    elif file_type in ["doc", "docx"]:
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_type in ["ppt", "pptx"]:
        prs = Presentation(file)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text.strip()

    return None

def run():
    st.header("🧠 AI File Analyzer")
    st.caption("Upload a file (PDF, DOCX, PPTX, TXT) and let AI analyze it.")

    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "doc", "docx", "ppt", "pptx"])
    if uploaded_file is not None:
        ext = uploaded_file.name.split(".")[-1].lower()
        text = extract_text_from_file(uploaded_file, ext)

        if not text:
            st.error("❌ Could not extract text from the uploaded file.")
            return

        st.subheader("📄 Extracted Text")
        st.text_area("Text:", value=text[:5000], height=300)  # Preview first 5000 chars

        model_options = [
            "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
            "DeepSeek-R1-0528",
            "Qwen3-235B-A22B-FP8",
        ]
        selected_model = st.selectbox("Choose an AI model:", model_options)

        prompt_instruction = st.text_area(
            "What do you want the AI to do with this content?",
            value="Summarize the content.",
            height=100,
        )

        if st.button("Analyze"):
            with st.spinner("Analyzing file..."):
                try:
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[{"role": "user", "content": f"{prompt_instruction}\n\n{text}"}],
                    )
                    output = response.choices[0].message.content
                    st.subheader("🔍 AI Analysis")
                    st.write(output)
                except Exception as e:
                    st.error(f"Error: {e}")
