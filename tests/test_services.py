# Unit tests for business logic functions in services.py
# Tests edge cases, parameterized scenarios, and error conditions

import pytest

from app.services import calculate_percentage, is_positive, summarize


class TestSummarize:
    """Test cases for the summarize function."""

    def test_summarize_typical_case(self):
        """Test summarize with typical input values."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = summarize(values)

        assert result["count"] == 5
        assert result["mean"] == 3.0
        assert result["min"] == 1.0
        assert result["max"] == 5.0

    def test_summarize_single_value(self):
        """Test summarize with a single value."""
        values = [42.5]
        result = summarize(values)

        assert result["count"] == 1
        assert result["mean"] == 42.5
        assert result["min"] == 42.5
        assert result["max"] == 42.5

    def test_summarize_negative_numbers(self):
        """Test summarize with negative numbers."""
        values = [-5.0, -2.0, 0.0, 3.0, 8.0]
        result = summarize(values)

        assert result["count"] == 5
        assert result["mean"] == 0.8
        assert result["min"] == -5.0
        assert result["max"] == 8.0

    def test_summarize_floating_point_precision(self):
        """Test summarize with floating point precision issues."""
        values = [0.1, 0.2, 0.3]
        result = summarize(values)

        assert result["count"] == 3
        # Allow for floating point precision
        assert abs(result["mean"] - 0.2) < 1e-10
        assert result["min"] == 0.1
        assert result["max"] == 0.3

    def test_summarize_large_values(self):
        """Test summarize with large numbers."""
        values = [1e6, 2e6, 3e6, 4e6, 5e6]
        result = summarize(values)

        assert result["count"] == 5
        assert result["mean"] == 3e6
        assert result["min"] == 1e6
        assert result["max"] == 5e6

    def test_summarize_duplicate_values(self):
        """Test summarize with duplicate values."""
        values = [5.0, 5.0, 5.0]
        result = summarize(values)

        assert result["count"] == 3
        assert result["mean"] == 5.0
        assert result["min"] == 5.0
        assert result["max"] == 5.0

    def test_summarize_empty_list_raises_error(self):
        """Test that summarize raises ValueError for empty list."""
        with pytest.raises(ValueError, match="Cannot summarize an empty list"):
            summarize([])

    @pytest.mark.parametrize(
        "values,expected_mean,expected_min,expected_max",
        [
            ([1, 2, 3], 2.0, 1, 3),
            ([10, 20, 30, 40], 25.0, 10, 40),
            ([0.5, 1.5, 2.5], 1.5, 0.5, 2.5),
            ([-10, 0, 10], 0.0, -10, 10),
        ],
    )
    def test_summarize_parameterized(self, values, expected_mean, expected_min, expected_max):
        """Parameterized test for various input combinations."""
        result = summarize(values)

        assert result["count"] == len(values)
        assert result["mean"] == expected_mean
        assert result["min"] == expected_min
        assert result["max"] == expected_max


class TestIsPositive:
    """Test cases for the is_positive function."""

    def test_positive_number(self):
        """Test positive number returns True."""
        assert is_positive(5.0) is True
        assert is_positive(0.1) is True
        assert is_positive(1e6) is True

    def test_negative_number(self):
        """Test negative number returns False."""
        assert is_positive(-5.0) is False
        assert is_positive(-0.1) is False
        assert is_positive(-1e6) is False

    def test_zero(self):
        """Test zero returns False."""
        assert is_positive(0.0) is False

    @pytest.mark.parametrize(
        "value,expected",
        [
            (1, True),
            (-1, False),
            (0, False),
            (0.0001, True),
            (-0.0001, False),
            (999999, True),
            (-999999, False),
        ],
    )
    def test_is_positive_parameterized(self, value, expected):
        """Parameterized test for is_positive function."""
        assert is_positive(value) is expected


class TestCalculatePercentage:
    """Test cases for the calculate_percentage function."""

    def test_basic_percentage(self):
        """Test basic percentage calculation."""
        result = calculate_percentage(25, 100)
        assert result == 25.0

    def test_percentage_with_float(self):
        """Test percentage calculation with floats."""
        result = calculate_percentage(33.33, 100)
        assert abs(result - 33.33) < 0.01

    def test_percentage_greater_than_100(self):
        """Test percentage when part is greater than total."""
        result = calculate_percentage(150, 100)
        assert result == 150.0

    def test_percentage_zero_part(self):
        """Test percentage when part is zero."""
        result = calculate_percentage(0, 100)
        assert result == 0.0

    def test_percentage_zero_total_raises_error(self):
        """Test that zero total raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
            calculate_percentage(50, 0)

    def test_percentage_negative_values(self):
        """Test percentage calculation with negative values."""
        result = calculate_percentage(-25, 100)
        assert result == -25.0

        result = calculate_percentage(25, -100)
        assert result == -25.0

    @pytest.mark.parametrize(
        "part,total,expected",
        [
            (50, 200, 25.0),
            (75, 300, 25.0),
            (1, 3, 33.333333333333336),  # Allowing for floating point precision
            (100, 50, 200.0),
            (0, 1000, 0.0),
        ],
    )
    def test_calculate_percentage_parameterized(self, part, total, expected):
        """Parameterized test for calculate_percentage function."""
        result = calculate_percentage(part, total)
        assert abs(result - expected) < 1e-10
