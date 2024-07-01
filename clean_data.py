import pandas as pd
import sqlite3

file = "properties.jsonl"
data = pd.read_json(file, lines=True)

print(data.isnull().sum())

data = data.fillna({"bathroom": 0, "bedroom": 0})

data = data.drop_duplicates(subset=["property_id"])

data.to_csv("properties.csv", index=False)
