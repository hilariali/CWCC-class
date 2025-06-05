# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.header("🤖 AI Chatbot (Dummy Tool 1)")
    st.write("Chat with an AI assistant powered by your OpenAI API key.")

    # Initialize OpenAI client
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Initialize conversation history (including a system prompt)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Display existing messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**AI:** {msg['content']}")

    st.markdown("---")

    # Local variable for the new user message; no session-state key
    user_input = st.text_input("Your message:")

    if st.button("Send"):
        if user_input:
            # Append user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Call OpenAI ChatCompletion
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.chat_history,
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

            # Append assistant response to history
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_msg})

            # No explicit rerun needed; clicking the button triggers a rerun automatically
        else:
            st.warning("Please enter a message before sending.")
