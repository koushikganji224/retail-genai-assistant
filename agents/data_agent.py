import duckdb
import pandas as pd
import os

DATA_PATH = "data/raw"


# ---------- NORMALIZATION FUNCTIONS ----------

def normalize_amazon_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "Order ID": "order_id",
        "Date": "order_date",
        "Sales Channel ": "channel",
        "ship-state": "region",
        "ship-country": "country",
        "Category": "category",
        "SKU": "sku",
        "Style": "style",
        "Qty": "quantity",
        "Amount": "revenue",
        "currency": "currency",
        "B2B": "customer_type",
        "Fulfilment": "fulfilment"
    })

    # 🔑 TYPE CONVERSION (CRITICAL)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)

    df["source"] = "Amazon"

    return df[[
        "order_id",
        "order_date",
        "region",
        "country",
        "channel",
        "category",
        "sku",
        "style",
        "quantity",
        "revenue",
        "currency",
        "customer_type",
        "fulfilment",
        "source"
    ]]



def normalize_international_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "DATE": "order_date",
        "CUSTOMER": "customer",
        "SKU": "sku",
        "Style": "style",
        "PCS": "quantity",
        "GROSS AMT": "revenue"
    })

    # 🔑 TYPE CONVERSION (CRITICAL)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)

    df["source"] = "International"
    df["region"] = "International"
    df["country"] = "International"
    df["channel"] = "Export"
    df["currency"] = "INR"
    df["category"] = None
    df["customer_type"] = "B2C"
    df["fulfilment"] = "International"

    return df[[
        "order_date",
        "region",
        "country",
        "channel",
        "category",
        "sku",
        "style",
        "quantity",
        "revenue",
        "currency",
        "customer_type",
        "fulfilment",
        "source"
    ]]


# ---------- DATA LOADING ----------

def load_sales_data() -> pd.DataFrame:
    """
    Load and normalize all relevant sales CSV files
    """
    sales_frames = []

    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)
        file_lower = file.lower()

        if not file_lower.endswith(".csv"):
            continue

        try:
            df = pd.read_csv(file_path)

            # AMAZON SALES
            if "amazon sale report" in file_lower:
                sales_frames.append(normalize_amazon_sales(df))

            # INTERNATIONAL SALES
            elif "international sale report" in file_lower:
                sales_frames.append(normalize_international_sales(df))

            # OTHER FILES (intentionally ignored for analytics)
            else:
                continue

        except Exception as e:
            print(f"Skipping file {file}: {e}")

    if not sales_frames:
        raise Exception("No valid sales data files found")

    return pd.concat(sales_frames, ignore_index=True)


# ---------- SQL EXECUTION ----------

def extract_data(sql_query: str) -> pd.DataFrame:
    """
    Execute analytical SQL against in-memory DuckDB
    """
    con = duckdb.connect(database=":memory:")

    sales_df = load_sales_data()
    con.register("sales", sales_df)

    return con.execute(sql_query).fetchdf()
