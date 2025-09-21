# Business logic functions for calculation operations
# These pure functions are designed to be easily unit tested

import statistics


def summarize(values: list[float]) -> dict:
    """
    Calculate summary statistics for a list of numbers.

    Args:
        values: List of numeric values to analyze

    Returns:
        Dictionary containing count, mean, min, max

    Raises:
        ValueError: If the input list is empty
    """
    if not values:
        raise ValueError("Cannot summarize an empty list")

    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "min": min(values),
        "max": max(values),
    }


def is_positive(value: float) -> bool:
    """
    Check if a number is positive.

    Args:
        value: Number to check

    Returns:
        True if value > 0, False otherwise
    """
    return value > 0


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage of part relative to total.

    Args:
        part: The part value
        total: The total value

    Returns:
        Percentage as a float (0-100)

    Raises:
        ValueError: If total is zero
    """
    if total == 0:
        raise ValueError("Cannot calculate percentage with zero total")

    return (part / total) * 100
