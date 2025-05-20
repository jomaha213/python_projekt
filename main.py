import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Wczytanie danych
df = pd.read_csv("data/imdb_top_1000.csv")

# Tytuł aplikacji
st.title("🎬 Rekomendacje filmów")

# Wybór filmów przez użytkownika
selected = st.multiselect("Wybierz swoje ulubione filmy:", df["Series_Title"].tolist())

# Sprawdzenie, czy użytkownik wybrał filmy
if selected:
    # Filtrowanie danych dla wybranych filmów i sortowanie malejąco według Gross
    selected_df = df[df["Series_Title"].isin(selected)][["Series_Title", "Gross"]].sort_values(by="Gross", ascending=False)

    # Tworzenie wykresu słupkowego
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(selected_df["Series_Title"], selected_df["Gross"], color="red")
    
    # Dodanie tytułu i etykiet osi
    ax.set_title("Zysk wybranych filmów", fontsize=14)
    ax.set_xlabel("Tytuł filmu", fontsize=12)
    ax.set_ylabel("Zysk (w USD)", fontsize=12)
    
    # Obrót etykiet osi X dla lepszej czytelności
    plt.xticks(rotation=45, ha="right")
    
    # Dodanie siatki
    ax.grid(True, axis="y", linestyle="--", alpha=0.7)
    
    # Formatowanie osi Y (skracanie dużych liczb)
    def millions_formatter(x, pos):
        return f"{x / 1_000_000:.2f}M"  # Konwersja na miliony z 2 miejscami po przecinku
    ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    
    # Dodanie większego marginesu po prawej stronie
    plt.subplots_adjust(left=0.1, right=0.9)  # Zwiększenie miejsca po prawej
    
    # Dopasowanie układu
    plt.tight_layout()
    
    # Wyświetlenie wykresu w Streamlit
    st.pyplot(fig)

    # Opcjonalnie: Wyświetlenie tabeli z wybranymi filmami
    st.write("🎥 Wybrane filmy (posortowane według zysku):")
    st.table(selected_df[["Series_Title", "Gross"]])
else:
    st.write("Wybierz przynajmniej jeden film, aby zobaczyć wykres!")