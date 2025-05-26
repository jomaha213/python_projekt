import psycopg2
from dotenv import load_dotenv
import os
import streamlit as st
# Load environment variables from .env


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            host=st.secrets["DB_HOST"],
            port=st.secrets["DB_PORT"]
        )
        return conn
    except Exception as e:
        print(f"❌ Błąd połączenia z bazą danych: {e}")
        return None

def get_all_users():
    conn = connect_db()
    if conn is None:
        print("⚠️ Nie udało się połączyć z bazą danych.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            users = cur.fetchall()
            for user in users:
                print(user)
    except Exception as e:
        print(f"❌ Błąd zapytania: {e}")
    finally:
        conn.close()
        print("✅ Połączenie z bazą danych zostało zamknięte.")

