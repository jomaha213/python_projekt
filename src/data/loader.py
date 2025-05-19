import csv

with open('data/imdb_top_1000.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)

print("List of column names:", header)