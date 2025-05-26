import streamlit as st
from sign import sign # logika logowania
from main import show_dashboard


def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_dashboard()  # Pokaż dashboard tylko jeśli użytkownik zalogowany
        if st.button("Wyloguj"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    else:
        sign()  # Wywołaj ekran logowania/rejestracji

if __name__ == "__main__":
    main()