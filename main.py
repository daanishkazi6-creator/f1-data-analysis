from loader import load_dataset, explore_dataset
from cleaner import impute_missing_or_outliers, format_and_rename
from analyzer import (
    calculate_basic_stats,
    show_correlations,
    filter_by_min_points,
    add_derived_columns,
    classify_finishes_with_loop,
)
from visualizer import plot_distributions
from exceptions import DatasetDimensionError, EmptyFilterResultError, InvalidColumnError


def main():
    filepath = "results.csv"
    try:
        df = load_dataset(filepath)
        print("Dataset 'results.csv' loaded successfully!")
    except (FileNotFoundError, DatasetDimensionError, RuntimeError) as e:
        print(f"Startup Error: {e}")
        return

    while True:
        print("\n==========================================")
        print("   FORMULA 1 DATA ANALYSIS - MAIN MENU")
        print("==========================================")
        print("1. Initial Exploration (Head, Tail, Shape, Types)")
        print("2. Clean & Preprocess Data (Impute NaNs/Outliers, Rename, Types)")
        print("3. Exploratory Data Analysis (Mean, Median, Std Dev & Correlations)")
        print("4. Visualizations (Histogram & Box Plot)")
        print("5. Data Manipulation (Filter, Derived Column & Row Loop)")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        try:
            if choice == "1":
                explore_dataset(df)

            elif choice == "2":
                df = impute_missing_or_outliers(df)
                df = format_and_rename(df)

            elif choice == "3":
                calculate_basic_stats(df)
                show_correlations(df)

            elif choice == "4":
                print("Available numeric columns: grid, position_order, points, laps, fastest_lap_speed")
                col = input("Enter column name to plot: ").strip()
                plot_distributions(df, col)

            elif choice == "5":
                min_pts = float(input("Enter minimum points to filter by (e.g., 10): "))
                filter_by_min_points(df, min_pts)
                df = add_derived_columns(df)
                classify_finishes_with_loop(df)

            elif choice == "6":
                print("Exiting program. Goodbye!")
                break

            else:
                print("Invalid option. Please enter a number from 1 to 6.")

        except (EmptyFilterResultError, InvalidColumnError) as custom_err:
            print(f"Analysis Alert: {custom_err}")
        except ValueError:
            print("Input Error: Please enter a valid numeric value.")
        except Exception as e:
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()