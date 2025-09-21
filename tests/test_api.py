# Integration tests for API endpoints
# Tests the complete API flow including request/response validation and error handling

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Integration tests for the root endpoint."""

    def test_root_endpoint_returns_info(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["message"] == "Calculation Service API"
        assert data["version"] == "1.0.0"
        assert "/health" in data["endpoints"]
        assert "/calc/summarize" in data["endpoints"]


class TestSummarizeEndpoint:
    """Integration tests for the summarize calculation endpoint."""

    def test_summarize_valid_request(self):
        """Test summarize endpoint with valid request."""
        request_data = {"values": [1.0, 2.0, 3.0, 4.0, 5.0]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert "count" in data
        assert "mean" in data
        assert "min" in data
        assert "max" in data

        assert data["count"] == 5
        assert data["mean"] == 3.0
        assert data["min"] == 1.0
        assert data["max"] == 5.0

    def test_summarize_single_value(self):
        """Test summarize endpoint with single value."""
        request_data = {"values": [42.5]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["count"] == 1
        assert data["mean"] == 42.5
        assert data["min"] == 42.5
        assert data["max"] == 42.5

    def test_summarize_negative_numbers(self):
        """Test summarize endpoint with negative numbers."""
        request_data = {"values": [-5.0, -2.0, 0.0, 3.0, 8.0]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["count"] == 5
        assert data["mean"] == 0.8
        assert data["min"] == -5.0
        assert data["max"] == 8.0

    def test_summarize_floating_point_precision(self):
        """Test summarize endpoint with floating point numbers."""
        request_data = {"values": [0.1, 0.2, 0.3]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["count"] == 3
        assert abs(data["mean"] - 0.2) < 1e-10
        assert data["min"] == 0.1
        assert data["max"] == 0.3

    def test_summarize_large_numbers(self):
        """Test summarize endpoint with large numbers."""
        request_data = {"values": [1e6, 2e6, 3e6]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["count"] == 3
        assert data["mean"] == 2e6
        assert data["min"] == 1e6
        assert data["max"] == 3e6

    def test_summarize_empty_list_validation_error(self):
        """Test summarize endpoint with empty list returns 422."""
        request_data = {"values": []}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

    def test_summarize_missing_values_field(self):
        """Test summarize endpoint with missing values field."""
        request_data = {}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

    def test_summarize_invalid_data_types(self):
        """Test summarize endpoint with invalid data types."""
        # Test with strings instead of numbers
        request_data = {"values": ["1", "2", "3"]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

        # Test with mixed types
        request_data = {"values": [1, "2", 3]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

        # Test with boolean values (which are technically int subclass)
        request_data = {"values": [1, True, 3]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

        # Test with null/None values
        request_data = {"values": [1, None, 3]}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

    def test_summarize_wrong_method(self):
        """Test summarize endpoint with wrong HTTP method."""
        request_data = {"values": [1, 2, 3]}

        # GET should not work
        response = client.get("/calc/summarize", params=request_data)
        assert response.status_code == 405

        # PUT should not work
        response = client.put("/calc/summarize", json=request_data)
        assert response.status_code == 405

        # DELETE should not work
        response = client.delete("/calc/summarize")
        assert response.status_code == 405

    def test_summarize_content_type_validation(self):
        """Test summarize endpoint content type validation."""
        request_data = {"values": [1, 2, 3]}

        # Valid JSON should work
        response = client.post(
            "/calc/summarize", json=request_data, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200

        # Invalid content type should fail
        response = client.post(
            "/calc/summarize", data="invalid data", headers={"Content-Type": "text/plain"}
        )
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "values,expected_count,expected_mean,expected_min,expected_max",
        [
            ([1, 2, 3], 3, 2.0, 1, 3),
            ([10, 20, 30, 40], 4, 25.0, 10, 40),
            ([0.5, 1.5, 2.5], 3, 1.5, 0.5, 2.5),
            ([-10, 0, 10], 3, 0.0, -10, 10),
            ([100, 200, 300, 400, 500], 5, 300.0, 100, 500),
        ],
    )
    def test_summarize_parameterized(
        self, values, expected_count, expected_mean, expected_min, expected_max
    ):
        """Parameterized integration test for summarize endpoint."""
        request_data = {"values": values}
        response = client.post("/calc/summarize", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["count"] == expected_count
        assert data["mean"] == expected_mean
        assert data["min"] == expected_min
        assert data["max"] == expected_max


class TestAPIErrorHandling:
    """Integration tests for API error handling."""

    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

        response = client.post("/nonexistent")
        assert response.status_code == 404

    def test_malformed_json(self):
        """Test that malformed JSON returns appropriate error."""
        response = client.post(
            "/calc/summarize", data="invalid json{", headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
