import streamlit as st
import openai

# Image Generator Instructions (system prompt)
PREPROMPT = """
# Image Generator Instructions

You are an image generator. The user provides a prompt plus optional style hints. Please infer the following parameters for image generation:

- **Prompt:** [prompt, max 50 words]
- **Style:** [style hint, optional]
- **Seed:** [seed]
- **Width:** [width]
- **Height:** [height]
- **Model:** [model]

## Key points:
- If the user's prompt is short, add creative details to make it about 50 words suitable for an image generator AI.
- Styles can be used to tweak the look, e.g., '3D', 'realism', 'outline', 'black and white'.
- Each seed value creates a unique image for a given prompt.
- To create variations of an image without changing its content:
  - Keep the prompt and style the same, change only the seed.
- To alter the content of an image:
  - Modify the prompt or style, keep the seed unchanged.
- Infer width and height around 1024×1024 or other aspect ratios if it makes sense.
- Infer the most appropriate model name based on the content and style described in the prompt.

## Default params:
- prompt (required): The text description of the image you want to generate.
- style (optional): Desired style. Options: ['None','3D','realism','outline','black and white'] (default: 'None')
- image_model (optional): The image-generation model. Options: ['flux','flux-realism','any-dark','flux-anime','flux-3d','turbo'] (default: 'flux')
- chat_model (optional): The LLM for processing. Options: ['DeepSeek-R1-0528','Meta-Llama-4-Maverick-17B-128E-Instruct-FP8','Qwen3-235B-A22B-FP8'] (default: 'DeepSeek-R1-0528')
- seed (optional): Seed for reproducible results (default: random).
- width/height (optional): Default 1024×1024.
- nologo (optional): Set to true to disable the logo rendering. Always set nologo to true unless specified.
"""

def run():
    st.title("🤖 AI Image Generator")
    st.caption("Quickly generate an image or chat with the AI to refine it.")

    # Toggleable instructions
    with st.expander("Show/Hide Instructions", expanded=False):
        st.markdown(PREPROMPT)

    # ---- Initial image prompt & options ----
    st.header("Create a New Image")
    initial_prompt = st.text_area("Image Prompt (required)", height=80)

    with st.expander("Advanced Settings (optional)"):
        # Style options
        style = st.selectbox(
            "Style (optional):",
            ["None", "3D", "realism", "outline", "black and white"],
            index=0
        )
        # Select which model to use for image generation
        image_model = st.radio(
            "Image Model:",
            ["flux", "flux-realism", "any-dark", "flux-anime", "flux-3d", "turbo"],
            index=0
        )
        # Select which LLM to use for chat completions
        chat_model = st.selectbox(
            "Chat Model:",
            ["DeepSeek-R1-0528", "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8", "Qwen3-235B-A22B-FP8"],
            index=0
        )
        # Aspect ratio presets
        aspect = st.radio(
            "Size:",
            ["Square (1024×1024)", "Portrait (768×1024)", "Landscape (1024×768)"],
            index=0
        )
        size_map = {
            "Square (1024×1024)": (1024, 1024),
            "Portrait (768×1024)": (768, 1024),
            "Landscape (1024×768)": (1024, 768)
        }
        width, height = size_map[aspect]

        # Seed option
        use_seed = st.checkbox("Specify seed for reproducibility")
        seed = st.number_input("Seed value:", min_value=0, max_value=2**32-1, value=0) if use_seed else None

        # Disable logo toggle
        nologo = st.checkbox("Disable logo on output", value=True)

    # Generate image button
    if st.button("Generate Image") and initial_prompt:
        # Initialize state
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": PREPROMPT}]

        # Build params dictionary including style
        params = {
            "prompt": initial_prompt,
            "style": None if style == "None" else style,
            "model": image_model,
            "width": width,
            "height": height,
            "seed": seed,
            "nologo": nologo
        }

        # Call the chat API to get the inferred image markup
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        with st.spinner("Generating image..."):
            try:
                response = client.chat.completions.create(
                    model=chat_model,
                    messages=[
                        {"role": "system", "content": PREPROMPT},
                        {"role": "user", "content": str(params)}
                    ],
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

        # Store and display
        st.session_state.messages.append({"role": "user", "content": initial_prompt})
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

    # ---- Chat for refinements ----
    if "messages" in st.session_state:
        st.header("Chat & Refine")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        followup = st.chat_input("Add another instruction or ask for edits...")
        if followup:
            st.session_state.messages.append({"role": "user", "content": followup})
            st.chat_message("user").write(followup)
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            with st.spinner("AI is thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=chat_model,
                        messages=st.session_state.messages,
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
