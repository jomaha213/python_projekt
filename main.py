import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.recommender.movie_recommender import MovieRecommender
from src.data.loader import DataLoader
from src.visualization.movie_chart import MovieChart

# Wczytanie danych
try:
    loader = DataLoader("data/imdb_top_1000.csv")
    df = loader.load()
except FileNotFoundError:
    st.error("Nie znaleziono pliku danych!")
    st.stop()

# Konwersja kolumny Gross na liczby
df["Gross"] = pd.to_numeric(df["Gross"].replace("[,$]", "", regex=True), errors="coerce")

def show_dashboard():
    st.title("🎬 Statystyki twoich ulubionych filmów")

    selected = st.multiselect("Wybierz swoje ulubione filmy:", df["Series_Title"].tolist())

    if not selected:
        st.info("Wybierz filmy, aby zobaczyć rekomendacje i wykresy!")
        return

    # Inicjalizacja klasy do tworzenia wykresów
    chart = MovieChart(df)

    # Wyświetlanie rekomendacji
    st.header("🎯 Polecane filmy dla Ciebie")
    recommender = MovieRecommender(df)
    recommendations = recommender.recommend(selected, top_n=6)

    cols = st.columns(3)
    for i, (_, row) in enumerate(recommendations.iterrows()):
        with cols[i % 3]:
            try:
                st.image(row["Poster_Link"], width=100)
            except:
                st.image("https://via.placeholder.com/100", width=100, caption="Brak plakatu")
            st.markdown(f"**{row['Series_Title']}**")
            st.markdown(row["Genre"])

    # Wyświetlanie wykresów jeden pod drugim
    st.subheader("Zysk według gatunków")
    chart.create_left_chart(selected)

    st.subheader("Rozkład gatunków")
    chart.create_right_chart(selected)

    st.subheader("Zysk wybranych filmów")
    chart.create_bar_chart(selected)

if __name__ == "__main__":
    show_dashboard()