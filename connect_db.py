import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
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

