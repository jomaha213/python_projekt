import streamlit as st
from connect_db import connect_db
import hashlib

class LoginManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = connect_db()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def hash_password(self, password: str) -> str:
        
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_user(self, username, password):
        self.connect()
        if self.conn is None:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT password FROM users WHERE username = %s", (username,))
                result = cur.fetchone()
                if result:
                    stored_password = result[0]
                    return self.hash_password(password) == stored_password
                else:
                    return False
        finally:
            self.disconnect()

    def register_user(self, username, password):
        self.connect()
        if self.conn is None:
            st.error("Nie udało się połączyć z bazą danych.")
            return False
        try:
            with self.conn.cursor() as cur:
                # Sprawdź czy użytkownik już istnieje
                cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                if cur.fetchone():
                    st.error("Użytkownik o takiej nazwie już istnieje.")
                    return False
                
                hashed_pw = self.hash_password(password)
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed_pw)
                )
                self.conn.commit()
                st.success("Rejestracja zakończona pomyślnie!")
                return True
        except Exception as e:
            st.error(f"Błąd podczas rejestracji: {e}")
            return False
        finally:
            self.disconnect()

    def login_panel(self):
        st.title("Panel logowania")
        option = st.radio("Wybierz opcję", ["Zaloguj się", "Zarejestruj się"])

        username = st.text_input("Login")
        password = st.text_input("Hasło", type="password")

        if option == "Zaloguj się":
            if st.button("Zaloguj"):
                if self.verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Zalogowano jako {username}")
                    st.rerun()
                else:
                    st.error("Niepoprawny login lub hasło")
        else:
            if st.button("Zarejestruj"):
                if username and password:
                    self.register_user(username, password)
                else:
                    st.warning("Wypełnij oba pola!")

if __name__ == "__main__":
    manager = LoginManager()
    manager.login_panel()
