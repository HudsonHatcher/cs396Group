# cs396Group

This project aims to create a automated python-built software testing program that will run predesigned tests to assess the throughput, resource usage, and effiecency of the software to allow for easy debugging.

Simplified Tech Stack

Language: Python 3.10

Framework: FastAPI
 for building lightweight, async APIs

Testing: pytest
 with pytest-cov for coverage metrics

Database: SQLite (lightweight, file-based, no external setup)

Logging: Python logging (JSON/text logs for transparency)

Security: python-dotenv
 for secrets management

Dependencies: pip + requirements.txt

CI/CD: GitHub Actions (tests + lint + build + push)

Containerization: Docker, publishing images to GitHub Container Registry (GHCR)

DevOps Process Design
1. CI/CD Workflow

Tool: GitHub Actions

Pipeline Steps:

Run lint (ruff) and formatting checks (black).

Run static type checking (mypy).

Run automated tests (pytest with coverage).

Build a Docker image of the FastAPI app.

Push image to GitHub Container Registry (GHCR).

Triggers:

Pull Requests → Run full CI (lint + tests).

Push to main → CI + Docker build/publish.

Tags (v*.*.*) → Versioned Docker release.

2. Architecture Approach

Containers: FastAPI service packaged with Docker.

Distributed Components:

API service (FastAPI)

SQLite database (local persistence)

Testing framework integrated into CI/CD

Scalability: Docker images can be deployed on any container platform (local Docker, k8s, etc.).

3. Product & Process Approach

Branching Model: GitHub Flow

main = stable branch

Features → PR → Review + CI checks → Merge

Collaboration: Dev + QA both contribute to feature branches.

Code Review: At least one review required before merge.

Quality Gates: PRs blocked unless CI passes.

4. Monitoring & Reporting

Tests: pytest generates JUnit/coverage reports.

Logs: Structured JSON logs from FastAPI app.

Dashboards: GitHub Actions UI shows build/test history.

Artifacts: Coverage and test reports stored in workflow artifacts.

5. DevOps Culture

Automation-First: Everything—tests, builds, deploys—is automated.

Collaboration-Driven: Dev and QA share responsibility for testing and code quality.

Continuous Feedback: Every push/PR provides instant feedback.

Resilience: Failures in CI/CD prevent bad code from reaching production.

Getting Started
Run Locally
# Clone repo
git clone <repo-url>
cd cs396Group

# Setup virtual environment
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Start FastAPI app
uvicorn app.main:app --reload

# Run tests with coverage
pytest --cov=app

Run with Docker
# Build Docker image
docker build -t ghcr.io/<your-org-or-username>/cs396group:latest .

# Run container
docker run -p 8080:8080 ghcr.io/<your-org-or-username>/cs396group:latest

Folder Structure
.
├── app/                # FastAPI application code
├── tests/              # pytest unit/integration tests
├── scripts/            # helper scripts for testing/metrics
├── Dockerfile          # container build instructions
├── requirements.txt    # dependencies
└── .github/workflows/  # GitHub Actions CI/CD pipeline
