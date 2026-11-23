class DatasetDimensionError(Exception):
    """Raised when the dataset has fewer than 8 columns or 100 rows."""
    pass


class EmptyFilterResultError(Exception):
    """Raised when a user's filter condition returns zero rows."""
    pass


class InvalidColumnError(Exception):
    """Raised when a requested column does not exist in the DataFrame."""
    pass