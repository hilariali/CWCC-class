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
- Infer the most appropriate model name based on the prompt and style.

## Default params:
 - prompt (required): Text description (up to 50 words).
 - style (optional): Desired style, e.g., '3D', 'realism', 'outline', 'black and white'.
 - image_model (optional): 'flux', 'flux-realism', 'any-dark', 'flux-anime', 'flux-3d', 'turbo'.
 - chat_model (optional): 'meta-llama/Llama-3.3-70B-Instruct', 'DeepSeek-V3-1', 'gpt-oss-120b', 'Meta-Llama-3-1-8B-Instruct-FP8', 'Meta-Llama-4-Maverick-17B-128E-Instruct-FP8', 'Qwen3-235B-A22B-Instruct-2507-FP8'.
 - seed (optional): integer for reproducibility.
 - width/height (optional): Pixel dimensions, default 1024×1024.
 - nologo (optional): true to disable the logo.

## Additional instructions:
- Return an embedded markdown image tag with the generated URL, followed by the prompt in italic below.

## Example:
![sunset over mountains in watercolor style](https://image.pollinations.ai/prompt/sunset%20over%20mountains%20in%20watercolor?width=1024&height=1024)
*sunset over mountains in watercolor style*
"""

def run():
    st.title("🤖 AI Image Generator")
    st.caption("Generate an image quickly, then fine-tune via chat below.")

    # Instructions toggle
    with st.expander("Show/Hide Instructions", expanded=False):
        st.markdown(PREPROMPT)

    # New image section
    st.header("Create a New Image")
    # Style selection exposed
    style = st.selectbox("Style (optional):", ["None", "3D", "realism", "outline", "black and white"], index=0)
    initial_prompt = st.text_area("Image Prompt (required)", height=80)

    with st.expander("Advanced Settings (optional)"):
        image_model = st.radio("Image Model:", ["flux","flux-realism","any-dark","flux-anime","flux-3d","turbo"], index=0)
    chat_model = st.selectbox("Chat Model:", ["meta-llama/Llama-3.3-70B-Instruct","DeepSeek-V3-1","gpt-oss-120b","Meta-Llama-3-1-8B-Instruct-FP8","Meta-Llama-4-Maverick-17B-128E-Instruct-FP8","Qwen3-235B-A22B-Instruct-2507-FP8"], index=0)
        aspect = st.radio("Size:", ["Square (1024×1024)","Portrait (768×1024)","Landscape (1024×768)"], index=0)
        size_map = {
            "Square (1024×1024)": (1024, 1024),
            "Portrait (768×1024)": (768, 1024),
            "Landscape (1024×768)": (1024, 768)
        }
        width, height = size_map[aspect]
        use_seed = st.checkbox("Specify seed for reproducibility")
        seed = st.number_input("Seed value:", 0, 2**32-1, 0) if use_seed else None
        nologo = st.checkbox("Disable logo", value=True)

    # Generate image button
    if st.button("Generate Image") and initial_prompt:
        params = {
            "prompt": initial_prompt,
            "style": None if style == "None" else style,
            "model": image_model,
            "width": width,
            "height": height,
            "seed": seed,
            "nologo": nologo
        }
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        with st.spinner("Generating image..."):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.3-70B-Instruct",
                    messages=[
                        {"role": "system", "content": PREPROMPT},
                        {"role": "user", "content": str(params)}
                    ]
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"
        # Display the returned markdown image
        st.markdown(assistant_msg)
        # Initialize conversation history for refinements
        st.session_state.messages = [
            {"role": "system", "content": PREPROMPT},
            {"role": "user", "content": initial_prompt},
            {"role": "assistant", "content": assistant_msg}
        ]

    # Chat & refine
    if st.session_state.get("messages"):
        st.header("Chat & Refine")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        followup = st.chat_input("Add instructions to modify the image...")
        if followup:
            st.session_state.messages.append({"role": "user", "content": followup})
            st.chat_message("user").write(followup)
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            with st.spinner("Updating image..."):
                try:
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
