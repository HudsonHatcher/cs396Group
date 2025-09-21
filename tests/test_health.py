# E2E (End-to-End) tests for health endpoint
# Tests the complete application flow from HTTP request to response

from fastapi.testclient import TestClient

from app.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """E2E tests for the health check endpoint."""

    def test_health_endpoint_returns_ok(self):
        """Test that health endpoint returns 200 OK with correct structure."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert data["status"] == "ok"
        assert isinstance(data["version"], str)
        assert len(data["version"]) > 0

    def test_health_endpoint_response_schema(self):
        """Test that health endpoint response matches expected schema."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Verify all required fields are present
        required_fields = ["status", "version"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Verify data types
        assert isinstance(data["status"], str)
        assert isinstance(data["version"], str)

        # Verify status value
        assert data["status"] == "ok"

    def test_health_endpoint_performance(self):
        """Test that health endpoint responds quickly (basic performance check)."""
        import time

        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()

        assert response.status_code == 200
        # Health check should be very fast (less than 100ms)
        assert (end_time - start_time) < 0.1

    def test_health_endpoint_content_type(self):
        """Test that health endpoint returns correct content type."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_methods(self):
        """Test that health endpoint only accepts GET requests."""
        # GET should work
        response = client.get("/health")
        assert response.status_code == 200

        # Other methods should not work (405 Method Not Allowed)
        response = client.post("/health")
        assert response.status_code == 405

        response = client.put("/health")
        assert response.status_code == 405

        response = client.delete("/health")
        assert response.status_code == 405
