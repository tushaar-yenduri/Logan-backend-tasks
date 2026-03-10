"""
Pytest configuration and shared fixtures for unit tests.
"""
import os
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv

# Load environment variables for tests
load_dotenv()


@pytest.fixture
def mock_dynamodb_table():
    """
    Fixture to mock DynamoDB table for testing.
    Returns a MagicMock object that simulates DynamoDB table operations.
    """
    mock_table = MagicMock()
    return mock_table


@pytest.fixture
def mock_dynamodb_resource(mock_dynamodb_table):
    """
    Fixture to mock DynamoDB resource.
    Returns a mock resource with a table property.
    """
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_dynamodb_table
    return mock_dynamodb


@pytest.fixture
def sample_student_data():
    """
    Fixture providing sample student data for tests.
    """
    return {
        "student_id": "test-uuid-1234",
        "name": "Tushaar",
        "age": 22,
        "course": "Computer Science",
        "email": "tushaar@example.com",
        "enrollment_year": 2025,
        "is_active": True
    }


@pytest.fixture
def sample_student_create():
    """
    Fixture providing sample StudentCreate model data.
    """
    return {
        "name": "Tushaar",
        "age": 22,
        "course": "Computer Science",
        "email": "tushaar@example.com",
        "enrollment_year": 2025,
        "is_active": True
    }


@pytest.fixture
def sample_student_put():
    """
    Fixture providing sample StudentPut model data for full replacement.
    """
    return {
        "name": "John Doe",
        "age": 25,
        "course": "Mathematics",
        "email": "john@example.com",
        "enrollment_year": 2024,
        "is_active": False
    }


@pytest.fixture
def sample_student_patch():
    """
    Fixture providing sample StudentPatch model data for partial update.
    """
    return {
        "name": "Updated Name",
        "is_active": False
    }


@pytest.fixture
def mock_env_vars():
    """
    Fixture to mock environment variables.
    """
    with patch.dict(os.environ, {
        "AWS_REGION": "us-east-1",
        "AWS_ACCESS_KEY_ID": "test_key",
        "AWS_SECRET_ACCESS_KEY": "test_secret",
        "DYNAMODB_TABLE": "students",
        "SECRET_KEY": "test_secret_key",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30"
    }):
        yield

