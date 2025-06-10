import pandas as pd
import plotly.express as px
import streamlit as st

class MovieChart:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def format_gross(self, gross: float) -> str:
        if gross >= 1_000_000_000:
            return f"{gross / 1_000_000_000:.2f} mld"
        elif gross >= 1_000_000:
            return f"{gross / 1_000_000:.2f} mln"
        elif gross >= 1_000:
            return f"{gross / 1_000:.2f} tys."
        else:
            return str(int(gross))

    def create_bar_chart(self, selected: list) -> None:
        if not selected:
            st.write("Wybierz przynajmniej jeden film, aby zobaczyć wykres!")
            return

        selected_df = (
            self.df[self.df["Series_Title"].isin(selected)][["Series_Title", "Released_Year", "Gross"]]
            .dropna(subset=["Gross"])
            .sort_values(by="Gross", ascending=False)
        )

        if selected_df.empty:
            st.write("Wybrane filmy nie mają danych o zysku (Gross). Wybierz inne filmy!")
            return

        fig = px.bar(
            selected_df,
            x="Series_Title",
            y="Gross",
            color="Gross",
            color_continuous_scale=["red", "yellow", "green"],
            title="Zysk wybranych filmów",
            labels={"Series_Title": "Tytuł filmu", "Gross": "Zysk"},
        )

        selected_df["Formatted_Gross"] = selected_df["Gross"].apply(self.format_gross)

        fig.update_traces(
            hovertemplate=(
                "<b>Tytuł filmu:</b> %{x}<br>" +
                "<b>Zysk:</b> %{customdata[0]}<br>" +
                "<b>Rok wydania:</b> %{customdata[1]}<extra></extra>"
            ),
            customdata=selected_df[["Formatted_Gross", "Released_Year"]]
        )

        fig.update_layout(
            yaxis=dict(tickformat="~s", title="Zysk", showgrid=True, zeroline=True),
            xaxis=dict(title="Tytuł filmu"),
            title_font_size=14,
            xaxis_tickangle=45,
            showlegend=False,
            margin=dict(r=50),
            coloraxis_showscale=False,
        )

        st.plotly_chart(fig, use_container_width=True)

        selected_df.reset_index(drop=True, inplace=True)
        selected_df.index += 1

        st.write("🎥 Wybrane filmy (posortowane według zysku):")
        st.table(
            selected_df.reset_index()[["index", "Series_Title", "Released_Year", "Gross"]]
            .rename(columns={"index": "Lp."})
        )

    def create_left_chart(self, selected: list) -> None:
        """Tworzy wykres kołowy zysku według gatunków dla wybranych filmów."""
        if not selected:
            return

        selected_df = self.df[self.df["Series_Title"].isin(selected)][["Series_Title", "Genre", "Gross"]].dropna(subset=["Genre", "Gross"])

        if selected_df.empty:
            st.write("Brak danych o zysku lub gatunkach dla wybranych filmów.")
            return

        # Grupowanie zysków według gatunków i sumowanie
        genre_gross = selected_df.groupby("Genre")["Gross"].sum().reset_index()

        # Formatowanie zysku dla tooltipów
        genre_gross["Formatted_Gross"] = genre_gross["Gross"].apply(self.format_gross)

        fig = px.pie(
            genre_gross,
            names="Genre",
            values="Gross",
            title="Zysk według gatunków",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_traces(
            hovertemplate=(
                "<b>Gatunek:</b> %{label}<br>" +
                "<b>Zysk:</b> %{customdata[0]}<extra></extra>"
            ),
            customdata=genre_gross[["Formatted_Gross"]]
        )

        fig.update_layout(
            yaxis=dict(title="Zysk", showgrid=True),
            title_font_size=14,
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)

    def create_right_chart(self, selected: list) -> None:
        """Tworzy wykres punktowy po prawej stronie - IMDB_Rating vs Zysk netto."""
        if not selected:
            return

        selected_df = self.df[self.df["Series_Title"].isin(selected)][["Series_Title", "IMDB_Rating", "Gross"]].dropna(subset=["IMDB_Rating", "Gross"])

        if selected_df.empty:
            st.write("Brak danych o ocenach IMDB lub zysku dla wybranych filmów.")
            return

        # Formatowanie zysku dla tooltipa
        selected_df["Formatted_Gross"] = selected_df["Gross"].apply(self.format_gross)

        # Skracanie tytułów do 15 znaków z ... dla czytelności na wykresie
        selected_df["Short_Title"] = selected_df["Series_Title"].apply(lambda x: x[:15] + "..." if len(x) > 15 else x)

        fig = px.scatter(
            selected_df,
            x="IMDB_Rating",
            y="Gross",
            text="Short_Title",  # Użycie skróconych tytułów na wykresie
            title="Ocena IMDB vs Zysk netto",
            labels={"IMDB_Rating": "Ocena IMDB", "Gross": "Zysk netto"},
            hover_data=["Formatted_Gross", "Series_Title"],  # Pełne tytuły w tooltipach
        )

        # Dostosowanie etykiet tekstowych na wykresie
        fig.update_traces(
            textposition="top center",
            hovertemplate=(
                "<b>Tytuł:</b> %{customdata[1]}<br>" +  # Pełny tytuł z hover_data
                "<b>Ocena IMDB:</b> %{x}<br>" +
                "<b>Zysk netto:</b> %{customdata[0]}<extra></extra>"
            ),
            textfont=dict(size=10)  # Mniejszy rozmiar tekstu dla lepszej czytelności
        )

        fig.update_layout(
            yaxis=dict(tickformat="~s", title="Zysk netto", showgrid=True),
            xaxis=dict(title="Ocena IMDB", showgrid=True),
            title_font_size=14,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50),  # Zwiększenie marginesów dla lepszego rozmieszczenia
        )

        st.plotly_chart(fig, use_container_width=True)