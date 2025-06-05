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

    return ""

def run():
    st.header("🧠 Multi-File AI Analyzer")
    st.caption("Upload up to 10 files (TXT, PDF, DOCX, PPTX) and let AI analyze them together.")

    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )

    uploaded_files = st.file_uploader(
        "Upload files", type=["txt", "pdf", "doc", "docx", "ppt", "pptx"], accept_multiple_files=True
    )

    if uploaded_files:
        if len(uploaded_files) > 10:
            st.warning("⚠️ You can upload up to 10 files.")
            return

        full_text = ""
        for file in uploaded_files:
            ext = file.name.split(".")[-1].lower()
            extracted = extract_text_from_file(file, ext)
            if not extracted:
                st.error(f"Could not extract text from {file.name}")
                continue
            st.success(f"✅ Extracted: {file.name}")
            full_text += f"\n\n--- {file.name} ---\n\n{extracted}"

        st.subheader("📄 Combined Extracted Text Preview")
        st.text_area("Combined text (first 5000 characters):", value=full_text[:5000], height=300)

        model_options = [
            "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
            "DeepSeek-R1-0528",
            "Qwen3-235B-A22B-FP8",
        ]
        selected_model = st.selectbox("Choose an AI model:", model_options)

        prompt_instruction = st.text_area(
            "What should the AI do with the content?",
            value="Summarize all the files.",
            height=100,
        )

        if st.button("Analyze All Files"):
            with st.spinner("Analyzing..."):
                try:
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[{"role": "user", "content": f"{prompt_instruction}\n\n{full_text}"}],
                    )
                    st.subheader("🔍 AI Analysis Result")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
