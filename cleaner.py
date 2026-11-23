import pandas as pd
import numpy as np


def impute_missing_or_outliers(df):
    df_clean = df.copy()
    total_nans = df_clean.isna().sum().sum()

    if total_nans > 0:
        print(f"\nFound {total_nans} NaN values. Imputing with median (numeric) and mode (categorical)...")
        for col in df_clean.columns:
            if df_clean[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(df_clean[col]):
                    median_val = df_clean[col].median()
                    df_clean[col] = df_clean[col].fillna(median_val)
                else:
                    mode_val = df_clean[col].mode()[0]
                    df_clean[col] = df_clean[col].fillna(mode_val)
    else:
        print("\nNo NaN values found. Replacing values outside ±2 standard deviations...")
        for col in df_clean.select_dtypes(include=[np.number]).columns:
            mean_val = df_clean[col].mean()
            std_val = df_clean[col].std()
            lower_bound = mean_val - 2 * std_val
            upper_bound = mean_val + 2 * std_val
            median_val = df_clean[col].median()

            outliers = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
            df_clean.loc[outliers, col] = median_val

    return df_clean


def format_and_rename(df):
    df_formatted = df.copy()

    rename_map = {
        "resultId": "result_id",
        "raceId": "race_id",
        "driverId": "driver_id",
        "constructorId": "constructor_id",
        "positionText": "position_text",
        "positionOrder": "position_order",
        "fastestLap": "fastest_lap",
        "fastestLapTime": "fastest_lap_time",
        "fastestLapSpeed": "fastest_lap_speed",
        "statusId": "status_id",
    }
    df_formatted = df_formatted.rename(columns=rename_map)

    int_cols = ["number", "position", "fastest_lap"]
    for col in int_cols:
        if col in df_formatted.columns:
            df_formatted[col] = pd.to_numeric(df_formatted[col], errors="coerce").fillna(0).astype(int)

    if "fastest_lap_speed" in df_formatted.columns:
        df_formatted["fastest_lap_speed"] = pd.to_numeric(
            df_formatted["fastest_lap_speed"], errors="coerce"
        )

    print("Columns renamed and data types converted successfully.")
    return df_formatted