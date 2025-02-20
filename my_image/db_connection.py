import pandas as pd
import os
from sklearn.datasets import load_breast_cancer
from sqlalchemy import create_engine

data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df.columns = [column.replace(" ", "_") for column in df.columns]

df_data = (
    df
    .assign(target = data.target)
    .filter(items=["target"] + df.columns.tolist())
)

postgres_uri = os.environ["POSTGRES_URL"]

database = os.environ["POSTGRES_DB"]
table_name = "cancer_table"

engine = create_engine(postgres_uri)

df_data.to_sql(name=table_name, con=engine, if_exists="replace")
print(f"data Written to: {table_name} table in {database} database")

sql = "select * from cancer_table"
df = pd.read_sql_query(sql, engine)
print(df.head())