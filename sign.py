import streamlit as st
from login import LoginManager

def sign():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    manager = LoginManager()

    if not st.session_state.logged_in:
        st.title("Logowanie")
        option = st.radio("Wybierz opcję", ["Zaloguj się", "Zarejestruj się"])

        username = st.text_input("Login")
        password = st.text_input("Hasło", type="password")

        if option == "Zaloguj się":
            if st.button("Zaloguj"):
                if manager.verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Zalogowano jako {username}")
                    st.rerun()
                else:
                    st.error("Niepoprawny login lub hasło")
        else:
            if st.button("Zarejestruj"):
                if username and password:
                    manager.register_user(username, password)
                else:
                    st.warning("Wypełnij oba pola!")
            

    

if __name__ == "__main__":
    sign()
