# FastAPI application entry point with health and calculation endpoints

import importlib.metadata

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from .services import summarize

# Initialize FastAPI app
app = FastAPI(
    title="Calculation Service API",
    description="A robust API for mathematical calculations with comprehensive testing",
    version="1.0.0",
)


class SummarizeRequest(BaseModel):
    """Request model for summarize endpoint."""

    values: list[float] = Field(
        ..., description="List of numbers to analyze", min_length=1, examples=[[1.5, 2.3, 4.1, 3.7]]
    )

    model_config = {"strict": True}

    @field_validator("values")
    @classmethod
    def validate_values_strict(cls, v):
        """Ensure values are strictly numeric, rejecting string coercion."""
        if not isinstance(v, list):
            raise ValueError("Values must be a list")

        for i, item in enumerate(v):
            if not isinstance(item, (int, float)):
                raise ValueError(f"Item at index {i} must be a number, got {type(item).__name__}")
            if isinstance(item, bool):  # bool is a subclass of int in Python
                raise ValueError(f"Item at index {i} must be a number, not boolean")

        return v


class SummarizeResponse(BaseModel):
    """Response model for summarize endpoint."""

    count: int = Field(description="Number of values provided")
    mean: float = Field(description="Arithmetic mean of values")
    min: float = Field(description="Minimum value")
    max: float = Field(description="Maximum value")


class HealthResponse(BaseModel):
    """Response model for health endpoint."""

    status: str = Field(description="Service status")
    version: str = Field(description="Application version")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Calculation Service API",
        "version": "1.0.0",
        "endpoints": ["/health", "/calc/summarize", "/docs"],
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns service status and version information.
    """
    try:
        version = importlib.metadata.version("app")
    except importlib.metadata.PackageNotFoundError:
        version = "1.0.0"

    return HealthResponse(status="ok", version=version)


@app.post("/calc/summarize", response_model=SummarizeResponse)
async def calculate_summary(request: SummarizeRequest):
    """
    Calculate summary statistics for a list of numbers.

    Args:
        request: SummarizeRequest containing list of values

    Returns:
        SummarizeResponse with count, mean, min, max

    Raises:
        HTTPException: 422 for validation errors, 400 for business logic errors
    """
    result = summarize(request.values)
    return SummarizeResponse(**result)
