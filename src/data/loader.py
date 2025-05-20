import csv

with open('data/imdb_top_1000.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)

print("List of column names:", header)


class DataLoader:
    def __init__(self, path):
        self.path = path
        self.df = None

    def load(self):
        import pandas as pd
        self.df = pd.read_csv(self.path)
        return self.df

loader = DataLoader("data/imdb_top_1000.csv")
df = loader.load()
