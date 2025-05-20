import streamlit as st
import pandas as pd
import plotly.express as px

# Wczytanie danych
df = pd.read_csv("data/imdb_top_1000.csv")

# Konwersja kolumny Gross na liczby
df["Gross"] = df["Gross"].replace("[,$]", "", regex=True).astype(float)

# Tytuł aplikacji
st.title("🎬 Rekomendacje filmów")

# Wybór filmów przez użytkownika
selected = st.multiselect("Wybierz swoje ulubione filmy:", df["Series_Title"].tolist())

# Sprawdzenie, czy użytkownik wybrał filmy
if selected:
    # Filtrowanie danych dla wybranych filmów, usuwanie NaN i sortowanie malejąco według Gross
    selected_df = (
        df[df["Series_Title"].isin(selected)][["Series_Title", "Released_Year", "Gross"]]
        .dropna(subset=["Gross"])
        .sort_values(by="Gross", ascending=False)
    )

    # Sprawdzenie, czy po odfiltrowaniu coś zostało
    if not selected_df.empty:
        # Tworzenie wykresu słupkowego z Plotly i gradientem kolorów
        fig = px.bar(
            selected_df,
            x="Series_Title",
            y="Gross",
            color="Gross",
            color_continuous_scale=["red", "yellow", "green"],  # Gradient: czerwony → żółty → zielony
            title="Zysk wybranych filmów",
            labels={"Series_Title": "Tytuł filmu", "Gross": "Zysk"},
        )

        # Automatyczne dostosowanie osi Y
        fig.update_layout(
            yaxis=dict(
                tickformat="~s",  # Format SI (np. 100M, 1B)
                title="Zysk",
                showgrid=True,
                zeroline=True,
            ),
            xaxis=dict(
                title="Tytuł filmu",
            ),
            title_font_size=14,
            xaxis_tickangle=45,
            showlegend=False,
            margin=dict(r=50),
            coloraxis_showscale=False,
        )

        # Wyświetlenie wykresu w Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Dodanie kolumny z numerami porządkowymi
        selected_df.reset_index(drop=True, inplace=True)  # Reset indeksów dla poprawnej numeracji
        selected_df.index += 1  # Dodanie numeracji od 1

        # Wyświetlenie tabeli z numerami porządkowymi
        st.write("🎥 Wybrane filmy (posortowane według zysku):")
        st.table(selected_df.reset_index()[["index", "Series_Title", "Released_Year", "Gross"]].rename(columns={"index": "Lp."}))
    else:
        st.write("Wybrane filmy nie mają danych o zysku (Gross). Wybierz inne filmy!")
else:
    st.write("Wybierz przynajmniej jeden film, aby zobaczyć wykres!")
