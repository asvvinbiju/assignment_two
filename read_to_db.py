import pandas as pd
import sqlite3

data = pd.read_csv("properties.csv")

conn = sqlite3.connect("properties.db")

data.to_sql("properties", conn, if_exists="replace", index=False)

conn.close()
