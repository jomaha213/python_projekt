import streamlit as st
import pandas as pd
 #from src.recommender.simple_recommender import recommend

df = pd.read_csv("data/imdb_top_1000.csv")

st.title("🎬 Rekomendacje filmów")

selected = st.multiselect("Wybierz swoje ulubione filmy:", df["Series_Title"].tolist())

"""if selected:
    recs = recommend(df, selected)
    st.write("🎯 Rekomendacje:")
    st.table(recs[["Series_Title", "Genre", "IMDB_Rating"]])"""
