import pandas as pd
from sqlalchemy import create_engine

DB_USER = "exampleuser"
DB_PASS = "koivunen"  # sama kuin MySQL-käyttäjällä
DB_NAME = "exampledb"
DB_HOST = "localhost"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

df = pd.read_csv("data/global_temp_annual.csv")

print(df.head())

df.to_sql("global_temp", engine, if_exists="replace", index=False)

print("✅ Uploaded global_temp data to MySQL")
