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
        """Tworzy wykres kołowy po lewej stronie - zysk według gatunków."""
        if not selected:
            return

        selected_df = self.df[self.df["Series_Title"].isin(selected)][["Series_Title", "Genre", "Gross"]].dropna(subset=["Genre", "Gross"])

        if selected_df.empty:
            st.write("Brak danych o gatunkach lub zysku dla wybranych filmów.")
            return

        # Rozdzielanie gatunków (jeśli filmy mają wiele gatunków oddzielonych przecinkami)
        selected_df["Genre"] = selected_df["Genre"].str.split(", ")
        selected_df = selected_df.explode("Genre")

        # Sumowanie zysku dla każdego gatunku
        genre_gross = selected_df.groupby("Genre")["Gross"].sum().reset_index()

        if genre_gross.empty:
            st.write("Brak danych po grupowaniu według gatunków.")
            return

        # Formatowanie zysku do tooltipa
        genre_gross["Formatted_Gross"] = genre_gross["Gross"].apply(self.format_gross)

        fig = px.pie(
            genre_gross,
            names="Genre",
            values="Gross",
            title="Zysk według gatunków",
            labels={"Genre": "Gatunek", "Gross": "Zysk"},
            hover_data=["Formatted_Gross"],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )

        fig.update_layout(
            title_font_size=14,
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)

    def create_right_chart(self, selected: list) -> None:
        """Tworzy wykres kołowy po prawej stronie - rozkład gatunków."""
        if not selected:
            return

        selected_df = self.df[self.df["Series_Title"].isin(selected)][["Series_Title", "Genre"]].dropna(subset=["Genre"])

        if selected_df.empty:
            return

        selected_df["Genre"] = selected_df["Genre"].str.split(", ")
        selected_df = selected_df.explode("Genre")

        genre_counts = selected_df["Genre"].value_counts().reset_index()
        genre_counts.columns = ["Genre", "Count"]

        fig = px.pie(
            genre_counts,
            names="Genre",
            values="Count",
            title="Rozkład gatunków wybranych filmów",
        )

        fig.update_layout(
            title_font_size=14,
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)