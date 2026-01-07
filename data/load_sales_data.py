import pandas as pd
import os

def load_all_sales_data(folder="data/raw"):
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]

    if not files:
        raise Exception("No CSV files found in data/raw folder")

    dfs = []
    for file in files:
        path = os.path.join(folder, file)
        df = pd.read_csv(path) 
        df["source_file"] = file
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
