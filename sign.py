import streamlit as st
from login import LoginManager
# logowanie 
def sign():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    manager = LoginManager()

    if not st.session_state.logged_in:
        manager.login_panel()
               

if __name__ == "__main__":
    sign()
