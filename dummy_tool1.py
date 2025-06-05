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
            # If you need a custom endpoint, you can add:
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
    # 3) Define callback to send a message
    # ----------------------------------------------------------------------------
    def send_message():
        user_input = st.session_state.input_text.strip()
        if not user_input:
            return
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # Call the new OpenAI client API
        try:
            response = st.session_state.client.chat.completions.create(
                model="Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=st.session_state.chat_history,
            )
            assistant_msg = response.choices[0].message.content
        except Exception as e:
            assistant_msg = f"Error: {e}"
        # Append AI’s response
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_msg})
        # Clear the input box
        st.session_state.input_text = ""

    # ----------------------------------------------------------------------------
    # 4) Display existing conversation
    # ----------------------------------------------------------------------------
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**AI:** {msg['content']}")
    st.markdown("---")

    # ----------------------------------------------------------------------------
    # 5) Ensure the input key exists and render text_input
    # ----------------------------------------------------------------------------
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    st.text_input("Your message:", key="input_text")

    # ----------------------------------------------------------------------------
    # 6) “Send” button triggers the callback
    # ----------------------------------------------------------------------------
    st.button("Send", on_click=send_message)
