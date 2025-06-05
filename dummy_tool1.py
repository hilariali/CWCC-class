# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.header("🤖 AI Chatbot (Dummy Tool 1)")
    st.write("Chat with an AI assistant powered by your OpenAI API key.")

    # ----------------------------------------------------------------------------
    # 1) Initialize the new OpenAI client (v1.0.0+)
    # ----------------------------------------------------------------------------
    if "client" not in st.session_state:
        st.session_state.client = openai.OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
            # If you use a custom endpoint, uncomment and adjust below:
            # base_url="https://chatapi.akash.network/api/v1"
        )

    # ----------------------------------------------------------------------------
    # 2) Initialize conversation history in session_state
    # ----------------------------------------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # ----------------------------------------------------------------------------
    # 3) Let the user pick a model
    # ----------------------------------------------------------------------------
    model_options = [
        "DeepSeek-R1",
        "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
        "Qwen3-235B-A22B-FP8",
    ]
    selected_model = st.selectbox("Choose a model:", model_options)

    # ----------------------------------------------------------------------------
    # 4) Define function to send a message
    # ----------------------------------------------------------------------------
    def send_message():
        user_input = st.session_state.input_text.strip()
        if not user_input:
            return

        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call the OpenAI API with the selected model
        try:
            response = st.session_state.client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.chat_history,
            )
            assistant_msg = response.choices[0].message.content
        except Exception as e:
            assistant_msg = f"Error: {e}"

        # Append AI’s response
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_msg})

        # Clear the text area
        st.session_state.input_text = ""

    # ----------------------------------------------------------------------------
    # 5) Display existing conversation
    # ----------------------------------------------------------------------------
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**AI:** {msg['content']}")
    st.markdown("---")

    # ----------------------------------------------------------------------------
    # 6) Create a form so that pressing Enter submits
    # ----------------------------------------------------------------------------
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    with st.form(key="chat_form", clear_on_submit=False):
        st.text_area(
            "Your message:",
            key="input_text",
            height=100,      # Larger height for easier multi-line input
        )
        submitted = st.form_submit_button("Send")
        if submitted:
            send_message()
            # After send_message, the form will rerun and the text area will be cleared
