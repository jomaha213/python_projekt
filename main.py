import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("data/imdb_top_1000.csv")

# Tytuł aplikacji
st.title("🎬 Rekomendacje filmów")

# Wybór filmów przez użytkownika
selected = st.multiselect("Wybierz swoje ulubione filmy:", df["Series_Title"].tolist())

# Sprawdzenie, czy użytkownik wybrał filmy
if selected:
    # Filtrowanie danych dla wybranych filmów
    selected_df = df[df["Series_Title"].isin(selected)][["Series_Title", "IMDB_Rating"]]

    # Tworzenie wykresu słupkowego
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(selected_df["Series_Title"], selected_df["IMDB_Rating"], color="skyblue")
    
    # Dodanie tytułu i etykiet osi
    ax.set_title("Oceny IMDB wybranych filmów", fontsize=14)
    ax.set_xlabel("Tytuł filmu", fontsize=12)
    ax.set_ylabel("Ocena IMDB", fontsize=12)
    
    # Obrót etykiet osi X dla lepszej czytelności
    plt.xticks(rotation=45, ha="right")
    
    # Dodanie siatki
    ax.grid(True, axis="y", linestyle="--", alpha=0.7)
    
    # Dopasowanie układu
    plt.tight_layout()
    
    # Wyświetlenie wykresu w Streamlit
    st.pyplot(fig)

    # Opcjonalnie: Wyświetlenie tabeli z wybranymi filmami
    st.write("🎥 Wybrane filmy:")
    st.table(selected_df[["Series_Title", "IMDB_Rating"]])
else:
    st.write("Wybierz przynajmniej jeden film, aby zobaczyć wykres!")