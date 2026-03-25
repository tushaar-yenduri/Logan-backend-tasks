"""Simple integration-style tests against the students API."""

from typing import Any, Dict

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import Client, WSGITransport

from app.api import students as students_api
from app.core.security import create_access_token
from app.services.students_service import StudentService, get_student_service


_original_httpx_client_init = Client.__init__


def _patched_httpx_client_init(self, *args, **kwargs):
    app_target = kwargs.pop("app", None)
    if app_target is not None and "transport" not in kwargs:
        kwargs["transport"] = WSGITransport(app=app_target)
    return _original_httpx_client_init(self, *args, **kwargs)


Client.__init__ = _patched_httpx_client_init


class MockInsertOneResult:
    def __init__(self, inserted_id: str) -> None:
        self.inserted_id = inserted_id


class MockUpdateResult:
    def __init__(self, matched_count: int) -> None:
        self.matched_count = matched_count


class MockDeleteResult:
    def __init__(self, deleted_count: int) -> None:
        self.deleted_count = deleted_count


class MockCollection:
    """In-memory stand-in for a MongoDB collection."""

    def __init__(self) -> None:
        self._data: list[Dict[str, Any]] = []
        self._next_id = 1

    @staticmethod
    def _match_query(document: Dict[str, Any], query: Dict[str, Any]) -> bool:
        return all(document.get(key) == value for key, value in query.items())

    def find_one(self, query: Dict[str, Any]) -> Dict[str, Any] | None:
        for document in self._data:
            if self._match_query(document, query):
                return document.copy()
        return None

    def insert_one(self, document: Dict[str, Any]) -> MockInsertOneResult:
        record = document.copy()
        record["_id"] = str(self._next_id)
        self._next_id += 1
        self._data.append(record)
        return MockInsertOneResult(record["_id"])

    def find(self) -> list[Dict[str, Any]]:
        return [doc.copy() for doc in self._data]

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> MockUpdateResult:
        for document in self._data:
            if self._match_query(document, query):
                document.update(update.get("$set", {}))
                return MockUpdateResult(1)
        return MockUpdateResult(0)

    def delete_one(self, query: Dict[str, Any]) -> MockDeleteResult:
        for index, document in enumerate(self._data):
            if self._match_query(document, query):
                self._data.pop(index)
                return MockDeleteResult(1)
        return MockDeleteResult(0)


def _student_payload(name: str = "Jane Doe") -> Dict[str, Any]:
    return {
        "name": name,
        "age": 21,
        "course": "Computer Science",
        "skills": ["Python", "FastAPI"],
    }


@pytest.fixture
def mock_collection() -> MockCollection:
    return MockCollection()


@pytest.fixture
def student_service(mock_collection: MockCollection) -> StudentService:
    return StudentService(mock_collection)


@pytest.fixture
def test_app(student_service: StudentService) -> FastAPI:
    application = FastAPI()
    application.include_router(students_api.router)
    application.dependency_overrides[get_student_service] = lambda: student_service
    return application


@pytest.fixture
def client(test_app: FastAPI):
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> Dict[str, str]:
    token = create_access_token("admin")
    return {"Authorization": f"Bearer {token}"}


def test_create_student_success(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """The POST end-point should add a student and return the stored payload."""

    response = client.post("/students", json=_student_payload(), headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["message"] == "Student created successfully"
    assert body["student"]["name"] == "Jane Doe"


def test_create_student_validation_error(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """Missing required fields should raise a 422 from FastAPI."""

    response = client.post("/students", json={"name": "Short"}, headers=auth_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_student_duplicate(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """Submitting the same student twice should yield a 400 duplicate error."""

    payload = _student_payload()
    client.post("/students", json=payload, headers=auth_headers)
    response = client.post("/students", json=payload, headers=auth_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_get_students_empty(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """Requesting a student when none exist should return a 404 and 'Student not found'."""

    response = client.get("/students/ghost", headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Student not found"


def test_get_student_success(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """GET returns the student that was previously created."""

    payload = _student_payload()
    client.post("/students", json=payload, headers=auth_headers)
    response = client.get(f"/students/{payload['name']}", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["student"]["course"] == payload["course"]


def test_update_student_success(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """PUT changes the stored student fields."""

    payload = _student_payload()
    client.post("/students", json=payload, headers=auth_headers)
    response = client.put(
        f"/students/{payload['name']}",
        json={"course": "Algorithms"},
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["student"]["course"] == "Algorithms"


def test_update_student_not_found(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """Attempting to update a nonexistent student returns 404."""

    response = client.put(
        "/students/not-found",
        json={"course": "Algorithms"},
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_student_success(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """DELETE removes an existing student."""

    payload = _student_payload()
    client.post("/students", json=payload, headers=auth_headers)
    response = client.delete(f"/students/{payload['name']}", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Student deleted successfully"


def test_delete_student_not_found(client: TestClient, auth_headers: Dict[str, str]) -> None:
    """DELETEing a missing student returns 404."""

    response = client.delete("/students/missing", headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
