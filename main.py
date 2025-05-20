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
        .dropna(subset=["Gross"])  # Usuwamy filmy z brakującymi wartościami Gross
        .sort_values(by="Gross", ascending=False)
    )

    # Sprawdzenie, czy po odfiltrowaniu coś zostało
    if not selected_df.empty:
        # Tworzenie wykresu słupkowego z Plotly
        fig = px.bar(
            selected_df,
            x="Series_Title",
            y="Gross",
            color_discrete_sequence=["red"],  # Kolor słupków
            title="Zysk wybranych filmów",
            labels={"Series_Title": "Tytuł filmu", "Gross": "Zysk (w USD)"},
            hover_data={"Series_Title": True, "Released_Year": True, "Gross": ":,.2f"},  # Dane w tooltip
        )

        # Dostosowanie osi Y do formatu w milionach
        fig.update_layout(
            yaxis_tickformat=".2fM",  # Format w milionach
            yaxis_title="Zysk (w USD)",
            xaxis_title="Tytuł filmu",
            title_font_size=14,
            xaxis_tickangle=45,  # Obrót etykiet osi X
            showlegend=False,  # Ukrycie legendy
            margin=dict(r=50),  # Margines po prawej
        )

        # Wyświetlenie wykresu w Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Wyświetlenie tabeli z wybranymi filmami
        st.write("🎥 Wybrane filmy (posortowane według zysku):")
        st.table(selected_df[["Series_Title", "Released_Year", "Gross"]])
    else:
        st.write("Wybrane filmy nie mają danych o zysku (Gross). Wybierz inne filmy!")
else:
    st.write("Wybierz przynajmniej jeden film, aby zobaczyć wykres!")