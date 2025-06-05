# dummy_tool2.py

import streamlit as st
import openai

def run():
    st.header("🧠 AI File Analyzer")
    st.caption("Upload a text file and let AI analyze its contents.")

    # Initialize OpenAI Client
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )

    # File Upload
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        st.subheader("📄 File Contents")
        st.text_area("Text in file:", value=file_content, height=250)

        # Optional: Choose a model
        model_options = [
            "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
            "DeepSeek-R1-0528",
            "Qwen3-235B-A22B-FP8",
        ]
        selected_model = st.selectbox("Choose a model for analysis:", model_options)

        # Prompt input
        prompt_instruction = st.text_area(
            "What do you want the AI to do with this text?",
            value="Summarize the content.",
            height=100,
        )

        if st.button("Analyze File with AI"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": "user", "content": f"{prompt_instruction}\n\n{file_content}"}
                        ],
                    )
                    result = response.choices[0].message.content
                    st.success("✅ Analysis Complete")
                    st.subheader("🔍 AI Output")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
