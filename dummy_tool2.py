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
    st.title("📁 Chat with Your Files")
    st.caption("Upload documents (TXT, PDF, DOCX, PPTX) and ask questions about them using AI.")

    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )

    # Store session context
    if "file_context" not in st.session_state:
        st.session_state.file_context = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi! Upload your documents and ask me anything about them."}
        ]

    uploaded_files = st.file_uploader(
        "Upload up to 10 files", type=["txt", "pdf", "doc", "docx", "ppt", "pptx"], accept_multiple_files=True
    )

    if uploaded_files:
        if len(uploaded_files) > 10:
            st.warning("⚠️ Please upload no more than 10 files.")
            return

        combined_text = ""
        for file in uploaded_files:
            ext = file.name.split(".")[-1].lower()
            content = extract_text_from_file(file, ext)
            if content:
                combined_text += f"\n\n--- {file.name} ---\n{content}"
                st.success(f"✓ Extracted: {file.name}")
            else:
                st.error(f"Failed to extract text from: {file.name}")

        st.session_state.file_context = combined_text
        st.subheader("📄 File Text Preview")
        st.text_area("Combined Content (first 5000 characters)", value=combined_text[:5000], height=300)

    model_options = [
        "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
        "DeepSeek-R1-0528",
        "Qwen3-235B-A22B-FP8",
    ]
    selected_model = st.selectbox("Choose an AI model:", model_options)

    st.divider()

    # Show chat history
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # User prompt
    user_input = st.chat_input("Ask something about the files…")
    if user_input and st.session_state.file_context.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        with st.spinner("Thinking..."):
            try:
                # Combine file context with chat history
                context_prompt = (
                    f"You are an assistant that helps answer questions based on the following documents:\n\n"
                    f"{st.session_state.file_context}\n\n"
                    f"Now continue the conversation below."
                )
                full_history = [{"role": "system", "content": context_prompt}] + st.session_state.chat_history
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=full_history,
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error(f"Error: {e}")
    elif user_input:
        st.warning("Please upload files before chatting.")
