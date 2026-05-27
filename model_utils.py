import streamlit as st
import openai

def get_openai_client() -> openai.OpenAI:
    """
    Get the configured OpenAI-compatible client dynamically.
    First checks st.session_state (runtime updates), then falls back to st.secrets.
    """
    api_key = st.session_state.get("openai_api_key")
    if not api_key:
        api_key = st.secrets.get("OPENAI_API_KEY", "lm-studio")
        
    base_url = st.session_state.get("openai_base_url")
    if not base_url:
        base_url = st.secrets.get("OPENAI_BASE_URL")
        
    return openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )

def get_available_models(client=None) -> list[str]:
    """
    Fetch the list of loaded models from the endpoint.
    If the endpoint or API fails, returns an empty list.
    """
    if client is None:
        try:
            client = get_openai_client()
        except Exception as e:
            import logging
            logging.error(f"Error getting client: {e}")
            return []
            
    try:
        models = client.models.list()
        # Extract model IDs
        model_ids = [m.id for m in models.data]
        return model_ids
    except Exception as e:
        import logging
        logging.error(f"Error listing models: {e}")
        return []

def get_default_model(client=None, fallback="meta-llama/Llama-3.3-70B-Instruct") -> str:
    """
    Get the first available model from the endpoint, or fallback to the provided name.
    """
    if "selected_model" in st.session_state and st.session_state.selected_model:
        return st.session_state.selected_model
        
    models = get_available_models(client)
    if models:
        return models[0]
    return fallback
