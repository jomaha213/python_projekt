import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.recommender.movie_recommender import MovieRecommender
from src.data.loader import DataLoader
from src.visualization.movie_chart import MovieChart

# Wczytanie danych
loader = DataLoader("data/imdb_top_1000.csv")
df = loader.load()

# Konwersja kolumny Gross na liczby
df["Gross"] = df["Gross"].replace("[,$]", "", regex=True).astype(float)

def show_dashboard():
    # Tytuł aplikacji
    st.title("🎬 Statystyki twoich ulubionych filmów")

    # Wybór filmów przez użytkownika
    selected = st.multiselect("Wybierz swoje ulubione filmy:", df["Series_Title"].tolist())

    # Inicjalizacja klasy do tworzenia wykresów
    chart = MovieChart(df)

    # Wyświetlanie rekomendacji
    if selected:
        st.header("🎯 Polecane filmy dla Ciebie")
        recommender = MovieRecommender(df)
        recommendations = recommender.recommend(selected, top_n=6)

        cols = st.columns(3)
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with cols[i % 3]:
                st.image(row["Poster_Link"], width=100)
                st.markdown(f"**{row['Series_Title']}**")
                st.markdown(row["Genre"])

    # Tworzenie dwóch kolumn dla nowych wykresów
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Zysk według gatunków")
        chart.create_left_chart(selected)

    with col2:
        st.subheader("Rozkład gatunków")
        chart.create_right_chart(selected)

    # Istniejący wykres słupkowy poniżej
    st.subheader("Zysk wybranych filmów")
    chart.create_bar_chart(selected)

# Uruchomienie dashboardu
if __name__ == "__main__":
    show_dashboard()