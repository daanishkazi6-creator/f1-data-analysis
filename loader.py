import pandas as pd
import numpy as np
from exceptions import DatasetDimensionError


def load_dataset(filepath):
    try:
        df = pd.read_csv(filepath, na_values="\\N")
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the file at: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {e}")

    if df.shape[0] < 100 or df.shape[1] < 8:
        raise DatasetDimensionError(
            f"Dataset must have at least 100 rows and 8 columns. Found {df.shape}."
        )
    return df


def explore_dataset(df):
    print("\n--- FIRST 5 ROWS ---")
    print(df.head())

    print("\n--- LAST 5 ROWS ---")
    print(df.tail())

    print("\n--- DATASET DIMENSIONS ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\n--- DATA TYPES ---")
    print(df.dtypes)