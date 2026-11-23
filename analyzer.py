import numpy as np
import pandas as pd
from exceptions import EmptyFilterResultError, InvalidColumnError


def calculate_basic_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print("\n--- BASIC STATISTICS (MEAN, MEDIAN, STD DEV) ---")
    for col in numeric_cols:
        col_data = df[col].dropna().to_numpy()
        print(
            f"{col:20s} | Mean: {np.mean(col_data):10.2f} | "
            f"Median: {np.median(col_data):10.2f} | Std Dev: {np.std(col_data):10.2f}"
        )


def show_correlations(df):
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    print("\n--- CORRELATION MATRIX (KEY NUMERIC COLUMNS) ---")
    key_cols = [c for c in ["grid", "position_order", "points", "laps", "fastest_lap_speed"] if c in corr_matrix.columns]
    print(corr_matrix[key_cols].loc[key_cols].round(3))


def filter_by_min_points(df, min_points):
    if "points" not in df.columns:
        raise InvalidColumnError("Column 'points' is missing from the dataset.")

    filtered = df[df["points"] >= min_points]
    if filtered.empty:
        raise EmptyFilterResultError(f"No race results found with at least {min_points} points.")

    id_col = "result_id" if "result_id" in df.columns else "resultId"
    drv_col = "driver_id" if "driver_id" in df.columns else "driverId"
    pos_col = "position_order" if "position_order" in df.columns else "positionOrder"

    print(f"\nFound {len(filtered)} results with >= {min_points} points:")
    print(filtered[[id_col, drv_col, "grid", pos_col, "points"]].head(10))
    return filtered


def add_derived_columns(df):
    df_new = df.copy()
    pos_col = "position_order" if "position_order" in df_new.columns else "positionOrder"
    drv_col = "driver_id" if "driver_id" in df_new.columns else "driverId"

    df_new["positions_gained"] = df_new["grid"] - df_new[pos_col]
    print("\nCreated new column 'positions_gained' (grid - finishing position).")
    print(df_new[[drv_col, "grid", pos_col, "positions_gained"]].head(10))
    return df_new


def classify_finishes_with_loop(df):
    pos_col = "position_order" if "position_order" in df.columns else "positionOrder"
    podiums = 0
    points_finishes = 0
    outside_points = 0

    for _, row in df.iterrows():
        pos = row[pos_col]
        pts = row["points"]
        if pos <= 3:
            podiums += 1
        elif pts > 0:
            points_finishes += 1
        else:
            outside_points += 1

    print("\n--- FINISH CLASSIFICATION (COMPUTED VIA ROW LOOP) ---")
    print(f"Podium Finishes (Top 3): {podiums}")
    print(f"Other Points Finishes:   {points_finishes}")
    print(f"Outside Points:          {outside_points}")