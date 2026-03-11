from __future__ import annotations

import types

import pytest

import app.services.users_services as users_services


class UsersTableStub:
    def __init__(self) -> None:
        self.put_item_calls: list[dict] = []
        self.get_item_calls: list[dict] = []
        self.scan_calls: list[dict] = []
        self.delete_item_calls: list[dict] = []
        self.update_item_calls: list[dict] = []
        self._get_item_response: dict = {}
        self._scan_response: dict = {}

    def put_item(self, **kwargs):
        self.put_item_calls.append(kwargs)
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def get_item(self, **kwargs):
        self.get_item_calls.append(kwargs)
        return self._get_item_response

    def scan(self, **kwargs):
        self.scan_calls.append(kwargs)
        return self._scan_response

    def delete_item(self, **kwargs):
        self.delete_item_calls.append(kwargs)
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def update_item(self, **kwargs):
        self.update_item_calls.append(kwargs)
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}


def test_create_user_puts_item_and_returns_created(patcher) -> None:
    table_stub = UsersTableStub()
    patcher.setattr(users_services, "table", table_stub)

    # Make uuid deterministic for test.
    patcher.setattr(
        users_services,
        "uuid",
        types.SimpleNamespace(uuid4=lambda: "00000000-0000-0000-0000-000000000000"),
    )

    created = users_services.create_user({"name": "a", "age": 1})

    assert created["user_id"] == "00000000-0000-0000-0000-000000000000"
    assert created["name"] == "a"
    assert created["age"] == 1
    assert len(table_stub.put_item_calls) == 1
    assert table_stub.put_item_calls[0]["Item"] == created


def test_get_user_returns_item_or_none(patcher) -> None:
    table_stub = UsersTableStub()
    patcher.setattr(users_services, "table", table_stub)

    table_stub._get_item_response = {"Item": {"user_id": "u1"}}
    assert users_services.get_user("u1") == {"user_id": "u1"}
    assert table_stub.get_item_calls[-1] == {"Key": {"user_id": "u1"}}

    table_stub._get_item_response = {}
    assert users_services.get_user("missing") is None


def test_get_user_by_username_scans_and_returns_first(patcher) -> None:
    table_stub = UsersTableStub()
    patcher.setattr(users_services, "table", table_stub)

    table_stub._scan_response = {"Items": []}
    assert users_services.get_user_by_username("bob") is None
    assert len(table_stub.scan_calls) == 1
    assert table_stub.scan_calls[0]["Limit"] == 1

    table_stub._scan_response = {"Items": [{"user_id": "u1"}, {"user_id": "u2"}]}
    assert users_services.get_user_by_username("bob") == {"user_id": "u1"}


def test_delete_user_calls_delete_item(patcher) -> None:
    table_stub = UsersTableStub()
    patcher.setattr(users_services, "table", table_stub)

    users_services.delete_user("u1")
    assert table_stub.delete_item_calls == [{"Key": {"user_id": "u1"}}]


def test_update_user_empty_data_no_update_call(patcher) -> None:
    table_stub = UsersTableStub()
    patcher.setattr(users_services, "table", table_stub)

    users_services.update_user("u1", {})
    assert table_stub.update_item_calls == []


def test_update_user_builds_expression_and_calls_update(patcher) -> None:
    table_stub = UsersTableStub()
    patcher.setattr(users_services, "table", table_stub)

    users_services.update_user("u1", {"name": "new", "age": 2})
    assert len(table_stub.update_item_calls) == 1

    call = table_stub.update_item_calls[0]
    assert call["Key"] == {"user_id": "u1"}
    assert call["UpdateExpression"].startswith("SET ")

    # Verify that both fields are represented (order doesn't matter).
    update_expr = call["UpdateExpression"].removeprefix("SET ").split(", ")
    assert set(update_expr) == {"#name = :name", "#age = :age"}
    assert call["ExpressionAttributeValues"][":name"] == "new"
    assert call["ExpressionAttributeValues"][":age"] == 2
    assert call["ExpressionAttributeNames"]["#name"] == "name"
    assert call["ExpressionAttributeNames"]["#age"] == "age"

