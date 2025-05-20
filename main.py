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
            color="Gross",  # Kolor słupków zależny od wartości Gross
            color_continuous_scale=["red", "green"],  # Gradient od czerwonego (niski Gross) do zielonego (wysoki Gross)
            title="Zysk wybranych filmów",
            labels={"Series_Title": "Tytuł filmu", "Gross": "Zysk (w USD)"},
        )

        # Funkcja do formatowania zysku w tooltipie (mln lub mld)
        def format_gross(gross):
            if gross >= 1_000_000_000:
                return f"{gross / 1_000_000_000:.2f} mld"
            else:
                return f"{gross / 1_000_000:.2f} mln"

        # Dodanie sformatowanego zysku jako nowej kolumny do tooltipa
        selected_df["Formatted_Gross"] = selected_df["Gross"].apply(format_gross)

        # Dostosowanie tooltipów z wytłuszczeniem kategorii i sformatowanym zyskiem
        fig.update_traces(
            hovertemplate=(
                "<b>Tytuł filmu:</b> %{x}<br>" +
                "<b>Zysk:</b> %{customdata[0]}<br>" +
                "<b>Rok wydania:</b> %{customdata[1]}<extra></extra>"
            ),
            customdata=selected_df[["Formatted_Gross", "Released_Year"]]
        )

        # Dostosowanie osi i stylu
        fig.update_layout(
            yaxis_tickformat=".2fM",
            yaxis_title="Zysk (w USD)",
            xaxis_title="Tytuł filmu",
            title_font_size=14,
            xaxis_tickangle=45,
            showlegend=False,
            margin=dict(r=50),
            coloraxis_showscale=False,  # Ukrycie paska kolorów (opcjonalne)
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