import matplotlib.pyplot as plt
from exceptions import InvalidColumnError


def plot_distributions(df, column_name):
    if column_name not in df.columns:
        raise InvalidColumnError(f"Column '{column_name}' does not exist.")

    data = df[column_name].dropna()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(data, bins=25, color="steelblue", edgecolor="black")
    axes[0].set_title(f"Histogram of {column_name}")
    axes[0].set_xlabel(column_name)
    axes[0].set_ylabel("Frequency")

    axes[1].boxplot(data, vert=True)
    axes[1].set_title(f"Box Plot of {column_name}")
    axes[1].set_ylabel(column_name)

    plt.tight_layout()
    plt.show()