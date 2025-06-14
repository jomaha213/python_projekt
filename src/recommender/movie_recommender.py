import sys
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.loader import DataLoader

loader = DataLoader("data/imdb_top_1000.csv")
df = loader.load()



class MovieRecommender:
    def __init__(self, df):
        self.df = df.copy()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.feature_matrix = self._prepare_feature_matrix()

    def _prepare_feature_matrix(self):
        self.df["combined"] = (
            self.df["Genre"].fillna('') + ' ' +
            self.df["Director"].fillna('') + ' ' +
            self.df["Star1"].fillna('') + ' ' +  
            self.df["Star2"].fillna('') + ' ' +
            self.df["Overview"].fillna('')
        )
        return self.vectorizer.fit_transform(self.df["combined"])

    def recommend(self, selected_titles, top_n=5):
        # Indeksy ulubionych filmów
        indices = self.df[self.df['Series_Title'].isin(selected_titles)].index
        if len(indices) == 0:
            return []

        # Średni wektor preferencji
        mean_vector = self.feature_matrix[indices].mean(axis=0)
        mean_vector = np.array(mean_vector).reshape(1, -1)

        # podobieństwo z każdym filmem
        similarities = cosine_similarity(mean_vector, self.feature_matrix).flatten()

        self.df["similarity"] = similarities
        recommendations = self.df[~self.df["Series_Title"].isin(selected_titles)]
        recommendations = recommendations.sort_values(by="similarity", ascending=False)

        return recommendations.head(top_n)


recommender = MovieRecommender(df)
selected = ["The Dark Knight", "Inception"]
recs = recommender.recommend(selected, top_n=5)
print(recs[["Series_Title", "similarity"]])