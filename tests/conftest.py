import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app, activities

@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities before each test for isolation."""
    for activity in activities.values():
        activity['participants'].clear()
