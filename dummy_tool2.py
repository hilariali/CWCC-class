import streamlit as st

def run():
    st.header("🛠 Dummy Tool 2")
    st.write(
        """
        This is a placeholder for Dummy Tool 2.  
        Feel free to hook in any logic here in future.
        """
    )
    chk = st.checkbox("Click me! (Dummy Tool 2)")
    if chk:
        st.info("Checkbox selected, but there's no real logic behind it—just a demo.")
