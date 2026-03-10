"""
Unit tests for StudentService class.
"""
import uuid
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.models.students_model import StudentCreate, StudentPatch, StudentPut
from app.services.students_service import StudentService


class TestStudentService:
    """Test suite for StudentService class."""

    @pytest.fixture
    def service_with_mock(self, mock_dynamodb_resource, mock_env_vars):
        """
        Create a StudentService instance with mocked DynamoDB.
        """
        with patch("boto3.resource", return_value=mock_dynamodb_resource):
            service = StudentService()
            return service

    # --- Test create_student ---
    def test_create_student_success(self, service_with_mock, mock_dynamodb_table, sample_student_create):
        """Test successful student creation."""
        # Arrange
        mock_dynamodb_table.put_item.return_value = {}
        student = StudentCreate(**sample_student_create)

        # Act
        result = service_with_mock.create_student(student)

        # Assert
        assert "student_id" in result
        assert result["message"] == "Student created"
        assert result["data"]["name"] == sample_student_create["name"]
        mock_dynamodb_table.put_item.assert_called_once()

    def test_create_student_error(self, service_with_mock, mock_dynamodb_table, sample_student_create):
        """Test student creation with DynamoDB error."""
        # Arrange
        from botocore.exceptions import ClientError
        mock_dynamodb_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "Test error"}},
            "PutItem"
        )
        student = StudentCreate(**sample_student_create)

        # Act
        result = service_with_mock.create_student(student)

        # Assert
        assert "error" in result
        assert "Test error" in result["error"]

    # --- Test get_student ---
    def test_get_student_found(self, service_with_mock, mock_dynamodb_table, sample_student_data):
        """Test successful student retrieval."""
        # Arrange
        mock_dynamodb_table.get_item.return_value = {
            "Item": sample_student_data
        }

        # Act
        result = service_with_mock.get_student("test-uuid-1234")

        # Assert
        assert result is not None
        assert result["student_id"] == sample_student_data["student_id"]
        assert result["name"] == sample_student_data["name"]
        mock_dynamodb_table.get_item.assert_called_once_with(Key={"student_id": "test-uuid-1234"})

    def test_get_student_not_found(self, service_with_mock, mock_dynamodb_table):
        """Test student retrieval when student doesn't exist."""
        # Arrange
        mock_dynamodb_table.get_item.return_value = {}

        # Act
        result = service_with_mock.get_student("nonexistent-id")

        # Assert
        assert result is None

    def test_get_student_error(self, service_with_mock, mock_dynamodb_table):
        """Test student retrieval with DynamoDB error."""
        # Arrange
        from botocore.exceptions import ClientError
        mock_dynamodb_table.get_item.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Test error"}},
            "GetItem"
        )

        # Act
        result = service_with_mock.get_student("test-id")

        # Assert
        assert result is None

    # --- Test replace_student (PUT) ---
    def test_replace_student_success(self, service_with_mock, mock_dynamodb_table, sample_student_put):
        """Test successful student replacement."""
        # Arrange
        mock_dynamodb_table.put_item.return_value = {}
        student = StudentPut(**sample_student_put)

        # Act
        result = service_with_mock.replace_student("test-uuid-1234", student)

        # Assert
        assert result["message"] == "Student replaced successfully"
        assert result["data"]["student_id"] == "test-uuid-1234"
        assert result["data"]["name"] == sample_student_put["name"]
        mock_dynamodb_table.put_item.assert_called_once()

    def test_replace_student_error(self, service_with_mock, mock_dynamodb_table, sample_student_put):
        """Test student replacement with DynamoDB error."""
        # Arrange
        from botocore.exceptions import ClientError
        mock_dynamodb_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "Test error"}},
            "PutItem"
        )
        student = StudentPut(**sample_student_put)

        # Act
        result = service_with_mock.replace_student("test-uuid-1234", student)

        # Assert
        assert "error" in result

    # --- Test patch_student (PATCH) ---
    def test_patch_student_success(self, service_with_mock, mock_dynamodb_table, sample_student_patch, sample_student_data):
        """Test successful student patch."""
        # Arrange
        updated_data = sample_student_data.copy()
        updated_data.update(sample_student_patch)
        mock_dynamodb_table.update_item.return_value = {
            "Attributes": updated_data
        }
        student = StudentPatch(**sample_student_patch)

        # Act
        result = service_with_mock.patch_student("test-uuid-1234", student)

        # Assert
        assert result["message"] == "Student patched successfully"
        assert result["data"]["name"] == sample_student_patch["name"]
        mock_dynamodb_table.update_item.assert_called_once()

    def test_patch_student_no_changes(self, service_with_mock, mock_dynamodb_table):
        """Test student patch with no changes provided."""
        # Arrange
        student = StudentPatch()

        # Act
        result = service_with_mock.patch_student("test-uuid-1234", student)

        # Assert
        assert result["message"] == "No changes provided"
        mock_dynamodb_table.update_item.assert_not_called()

    def test_patch_student_error(self, service_with_mock, mock_dynamodb_table, sample_student_patch):
        """Test student patch with DynamoDB error."""
        # Arrange
        from botocore.exceptions import ClientError
        mock_dynamodb_table.update_item.side_effect = ClientError(
            {"Error": {"Code": "ValidationError", "Message": "Test error"}},
            "UpdateItem"
        )
        student = StudentPatch(**sample_student_patch)

        # Act
        result = service_with_mock.patch_student("test-uuid-1234", student)

        # Assert
        assert "error" in result

    # --- Test delete_student ---
    def test_delete_student_success(self, service_with_mock, mock_dynamodb_table):
        """Test successful student deletion."""
        # Arrange
        mock_dynamodb_table.delete_item.return_value = {}

        # Act
        result = service_with_mock.delete_student("test-uuid-1234")

        # Assert
        assert result["message"] == "Student deleted"
        mock_dynamodb_table.delete_item.assert_called_once_with(Key={"student_id": "test-uuid-1234"})

    def test_delete_student_error(self, service_with_mock, mock_dynamodb_table):
        """Test student deletion with DynamoDB error."""
        # Arrange
        from botocore.exceptions import ClientError
        mock_dynamodb_table.delete_item.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Test error"}},
            "DeleteItem"
        )

        # Act
        result = service_with_mock.delete_student("test-uuid-1234")

        # Assert
        assert "error" in result

    # --- Test _decimal_to_native ---
    def test_decimal_to_native_with_decimal(self, service_with_mock):
        """Test conversion of Decimal to native types."""
        # Arrange
        decimal_value = Decimal("22.5")

        # Act
        result = service_with_mock._decimal_to_native(decimal_value)

        # Assert
        assert result == 22.5

    def test_decimal_to_native_with_integer_decimal(self, service_with_mock):
        """Test conversion of whole number Decimal to int."""
        # Arrange
        decimal_value = Decimal("22")

        # Act
        result = service_with_mock._decimal_to_native(decimal_value)

        # Assert
        assert result == 22

    def test_decimal_to_native_with_list(self, service_with_mock):
        """Test conversion of list containing Decimals."""
        # Arrange
        data = [Decimal("1"), Decimal("2.5"), 3]

        # Act
        result = service_with_mock._decimal_to_native(data)

        # Assert
        assert result == [1, 2.5, 3]

    def test_decimal_to_native_with_dict(self, service_with_mock):
        """Test conversion of dict containing Decimals."""
        # Arrange
        data = {"age": Decimal("22"), "score": Decimal("95.5")}

        # Act
        result = service_with_mock._decimal_to_native(data)

        # Assert
        assert result == {"age": 22, "score": 95.5}

    def test_decimal_to_native_with_none(self, service_with_mock):
        """Test conversion with None value."""
        # Arrange
        data = None

        # Act
        result = service_with_mock._decimal_to_native(data)

        # Assert
        assert result is None

    def test_decimal_to_native_with_string(self, service_with_mock):
        """Test conversion with string value (should pass through)."""
        # Arrange
        data = "test string"

        # Act
        result = service_with_mock._decimal_to_native(data)

        # Assert
        assert result == "test string"

