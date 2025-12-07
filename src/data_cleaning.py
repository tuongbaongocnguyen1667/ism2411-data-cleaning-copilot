# File's name: data_cleaning.py
# Purpose: This script loads the raw sales dataset, performs standard cleaning steps (fixing column names, removing whitespace, handling missing or invalid values), and saves the cleaned data to data/processed/sales_data_clean.csv

import pandas as pd
from pathlib import Path

# Function 1 — LOAD DATA 
def load_data(file_path: str):
    """Load CSV data from a given file path."""
    return pd.read_csv(file_path)

# Function 2 — CLEAN COLUMN NAMES
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

# Function 3 — HANDLE MISSING VALUES (COPILOT FIXED)
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["price", "qty"]) #change from quantity to qty
    return df

# Function 4 — REMOVE INVALID ROWS (COPILOT ASSISTED)
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
# Convert to numeric (important fix for your error)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")

    # Drop rows where price or qty is missing after conversion
    df = df.dropna(subset=["price", "qty"])

    # Now safely filter for non-negative values
    df = df[(df["price"] >= 0) & (df["qty"] >= 0)]
    return df

# Additional cleaning step: strip whitespace from product/category
def strip_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    if "product" in df.columns:
        df["product"] = df["product"].astype(str).str.strip()
    if "category" in df.columns:
        df["category"] = df["category"].astype(str).str.strip()
    return df

# MAIN EXECUTION BLOCK
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())