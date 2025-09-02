import streamlit as st

def check_authentication():
    """
    Check if user is authenticated by verifying the passkey.
    Returns True if authenticated, False otherwise.
    """
    # Initialize authentication state if not exists
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    return st.session_state.authenticated

def authenticate_user():
    """
    Display authentication form and handle passkey verification.
    Returns True if successfully authenticated, False otherwise.
    """
    # Get passkey from secrets
    try:
        correct_passkey = st.secrets["general"]["PASSKEY"]
    except (KeyError, FileNotFoundError):
        # Fallback if secrets file doesn't exist
        correct_passkey = "2025"
    
    # Show authentication form
    st.title("🔐 Access Authentication")
    st.write("Please enter the passkey to access the CWCC AI-Tool Hub:")
    
    with st.form("auth_form"):
        passkey = st.text_input("Passkey:", type="password", help="Enter the provided passkey to access the application")
        submit_button = st.form_submit_button("Access Application")
        
        if submit_button:
            if passkey == correct_passkey:
                st.session_state.authenticated = True
                st.success("✅ Authentication successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid passkey. Please try again.")
                return False
    
    return False

def logout():
    """Logout the current user."""
    st.session_state.authenticated = False
    st.rerun()