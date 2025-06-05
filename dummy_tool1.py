# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.title("🤖 AI Chatbot")


    # ----------------------------------------------------------------------------
    # 1) Initialize the OpenAI client using secret
    # ----------------------------------------------------------------------------
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
        # If using a custom endpoint, include base_url="https://chatapi.akash.network/api/v1"
    )

    # ----------------------------------------------------------------------------
    # 2) Initialize or retrieve conversation history
    # ----------------------------------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    # ----------------------------------------------------------------------------
    # 3) Model selection (fixed at top of page)
    # ----------------------------------------------------------------------------
    model_options = [
        "DeepSeek-R1-0528",
        "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
        "Qwen3-235B-A22B-FP8",
    ]
    selected_model = st.selectbox("Choose a model:", model_options)

    # ----------------------------------------------------------------------------
    # 4) Display existing conversation using chat bubbles
    # ----------------------------------------------------------------------------
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # ----------------------------------------------------------------------------
    # 5) Handle new user input with st.chat_input()
    # ----------------------------------------------------------------------------
    prompt = st.chat_input("Type your message...")
    if prompt:
        # Append and show user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Call the API and show a spinner while waiting
        with st.spinner("AI is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages,
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

        # Append and display the assistant's reply
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        st.chat_message("assistant").write(assistant_msg)
