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
        """Tworzy wykres liniowy średniego zysku na film według dekad (lata 60, 70, 80, 90, 00)."""
        if not selected:
            return

        selected_df = self.df[self.df["Series_Title"].isin(selected)][["Series_Title", "Released_Year", "Gross"]].dropna(subset=["Released_Year", "Gross"])

        if selected_df.empty:
            st.write("Brak danych o zysku lub latach wydania dla wybranych filmów.")
            return

        # Konwersja roku na dekady
        selected_df = selected_df.copy()
        selected_df["Released_Year"] = selected_df["Released_Year"].astype(int)
        selected_df["Decade"] = pd.cut(selected_df["Released_Year"],
                                      bins=[1959, 1969, 1979, 1989, 1999, 2009],
                                      labels=["1960s", "1970s", "1980s", "1990s", "2000s"],
                                      right=True)

        # Obliczenie średniego zysku na film dla każdej dekady
        decade_gross = selected_df.groupby("Decade")["Gross"].mean().reset_index()

        if decade_gross.empty:
            st.write("Brak danych do wyświetlenia wykresu dla wybranych dekad.")
            return

        fig = px.line(
            decade_gross,
            x="Decade",
            y="Gross",
            title="Średni zysk na film według dekad",
            labels={"Decade": "Dekada", "Gross": "Średni zysk (mln)"},
            markers=True,
            color_discrete_sequence=["#1f77b4"]
        )

        fig.update_traces(
            hovertemplate="<b>Dekada:</b> %{x}<br><b>Średni zysk:</b> %{y:.2f} mln<extra></extra>"
        )

        fig.update_layout(
            yaxis=dict(tickformat="~s", title="Średni zysk (mln)", showgrid=True),
            xaxis=dict(title="Dekada"),
            title_font_size=14,
            showlegend=False,
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

        fig = px.scatter(
            selected_df,
            x="IMDB_Rating",
            y="Gross",
            text="Series_Title",  # Etykiety z tytułem filmu
            title="Ocena IMDB vs Zysk netto",
            labels={"IMDB_Rating": "Ocena IMDB", "Gross": "Zysk netto"},
            hover_data=["Formatted_Gross"],
        )

        # Dostosowanie etykiet tekstowych na wykresie
        fig.update_traces(
            textposition="top center",
            hovertemplate=(
                "<b>Tytuł:</b> %{text}<br>" +
                "<b>Ocena IMDB:</b> %{x}<br>" +
                "<b>Zysk netto:</b> %{customdata}<extra></extra>"
            ),
        )

        fig.update_layout(
            yaxis=dict(tickformat="~s", title="Zysk netto", showgrid=True),
            xaxis=dict(title="Ocena IMDB", showgrid=True),
            title_font_size=14,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)