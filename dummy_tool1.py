# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.header("🤖 AI Chatbot (Dummy Tool 1)")
    st.write("Chat with an AI assistant powered by your OpenAI API key.")

    # ----------------------------------------------------------------------------
    # 1) Initialize the new OpenAI client (v1.0.0+)
    # ----------------------------------------------------------------------------
    #
    # If you want to use the default OpenAI endpoint, simply do:
    #     client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    #
    # If you need to point at a custom base_url (e.g. chatapi.akash.network),
    # you can do exactly as in your test snippet:
    #
    #     client = openai.OpenAI(
    #         api_key=st.secrets["OPENAI_API_KEY"],
    #         base_url="https://chatapi.akash.network/api/v1"
    #     )
    #
    # (Uncomment whichever is appropriate below.)

    # ——— Default OpenAI endpoint ———
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    # ——— Custom base_url endpoint (uncomment if you use a custom server) ———
    # client = openai.OpenAI(
    #     api_key=st.secrets["OPENAI_API_KEY"],
    #     base_url="https://chatapi.akash.network/api/v1"
    # )

    # ----------------------------------------------------------------------------
    # 2) Initialize conversation history in session_state
    # ----------------------------------------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # ----------------------------------------------------------------------------
    # 3) Display the existing conversation
    # ----------------------------------------------------------------------------
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**AI:** {msg['content']}")

    st.markdown("---")

    # ----------------------------------------------------------------------------
    # 4) Text input for the next user message
    # ----------------------------------------------------------------------------
    user_input = st.text_input("Your message:")

    # ----------------------------------------------------------------------------
    # 5) When “Send” is clicked, append to history and call the new client API
    # ----------------------------------------------------------------------------
    if st.button("Send"):
        if not user_input:
            st.warning("Please enter a message before sending.")
        else:
            # 5a) Append the user’s message to session state
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # 5b) Call the new OpenAI endpoint:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # or whatever model you prefer
                    messages=st.session_state.chat_history
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

            # 5c) Append the assistant’s reply to session state
            st.session_state.chat_history.append(
                {"role": "assistant", "content": assistant_msg}
            )

            # No need for explicit rerun; Streamlit automatically re-runs after a button click
