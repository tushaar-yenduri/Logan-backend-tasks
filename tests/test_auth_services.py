from __future__ import annotations

import types

import pytest
from botocore.exceptions import ClientError

import app.services.auth_services as auth_services


class DynamoWaiterStub:
    def __init__(self) -> None:
        self.wait_calls: list[dict] = []

    def wait(self, **kwargs):
        self.wait_calls.append(kwargs)


class DynamoDbClientStub:
    class exceptions:
        class ResourceNotFoundException(Exception):
            pass

    def __init__(self) -> None:
        self.describe_table_calls: list[dict] = []
        self.create_table_calls: list[dict] = []
        self.waiter = DynamoWaiterStub()
        self._exists = True

    def describe_table(self, **kwargs):
        self.describe_table_calls.append(kwargs)
        if not self._exists:
            raise self.exceptions.ResourceNotFoundException("not found")
        return {"Table": {"TableName": kwargs.get("TableName")}}

    def create_table(self, **kwargs):
        self.create_table_calls.append(kwargs)
        return {"TableDescription": {"TableName": kwargs.get("TableName")}}

    def get_waiter(self, name: str):
        assert name == "table_exists"
        return self.waiter


class DynamoResourceStub:
    def __init__(self, client: DynamoDbClientStub) -> None:
        self.meta = types.SimpleNamespace(client=client)


class AuthUsersTableStub:
    def __init__(self) -> None:
        self.get_item_calls: list[dict] = []
        self.query_calls: list[dict] = []
        self.put_item_calls: list[dict] = []
        self._get_item_response: dict = {}
        self._query_response: dict = {}
        self._put_item_side_effect = None

    def get_item(self, **kwargs):
        self.get_item_calls.append(kwargs)
        return self._get_item_response

    def query(self, **kwargs):
        self.query_calls.append(kwargs)
        return self._query_response

    def put_item(self, **kwargs):
        self.put_item_calls.append(kwargs)
        if self._put_item_side_effect:
            raise self._put_item_side_effect
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}


def test_ensure_auth_users_table_noop_if_exists(patcher) -> None:
    client = DynamoDbClientStub()
    client._exists = True
    patcher.setattr(auth_services, "dynamodb", DynamoResourceStub(client))

    auth_services.ensure_auth_users_table()
    assert client.describe_table_calls == [{"TableName": "auth_users"}]
    assert client.create_table_calls == []
    assert client.waiter.wait_calls == []


def test_ensure_auth_users_table_creates_when_missing(patcher) -> None:
    client = DynamoDbClientStub()
    client._exists = False
    patcher.setattr(auth_services, "dynamodb", DynamoResourceStub(client))

    auth_services.ensure_auth_users_table()
    assert client.describe_table_calls == [{"TableName": "auth_users"}]
    assert len(client.create_table_calls) == 1
    assert client.create_table_calls[0]["TableName"] == "auth_users"
    assert client.waiter.wait_calls == [{"TableName": "auth_users"}]


def test_get_auth_user_by_id_returns_item_or_none(patcher) -> None:
    table = AuthUsersTableStub()
    patcher.setattr(auth_services, "auth_table", table)

    table._get_item_response = {"Item": {"user_id": "u1"}}
    assert auth_services.get_auth_user_by_id("u1") == {"user_id": "u1"}
    table._get_item_response = {}
    assert auth_services.get_auth_user_by_id("missing") is None


def test_get_auth_user_by_username_returns_first(patcher) -> None:
    table = AuthUsersTableStub()
    patcher.setattr(auth_services, "auth_table", table)

    table._query_response = {"Items": []}
    assert auth_services.get_auth_user_by_username("bob") is None

    table._query_response = {"Items": [{"user_id": "u1"}]}
    assert auth_services.get_auth_user_by_username("bob") == {"user_id": "u1"}
    assert table.query_calls[-1]["IndexName"] == "username-index"
    assert table.query_calls[-1]["Limit"] == 1


def test_create_auth_user_success(patcher) -> None:
    table = AuthUsersTableStub()
    patcher.setattr(auth_services, "auth_table", table)

    patcher.setattr(
        auth_services,
        "uuid",
        types.SimpleNamespace(uuid4=lambda: "11111111-1111-1111-1111-111111111111"),
    )

    created = auth_services.create_auth_user("bob", "hash", role="admin")
    assert created is not None
    assert created["user_id"] == "11111111-1111-1111-1111-111111111111"
    assert created["username"] == "bob"
    assert created["password_hash"] == "hash"
    assert created["role"] == "admin"
    assert len(table.put_item_calls) == 1
    assert table.put_item_calls[0]["Item"] == created


def test_create_auth_user_conditional_check_failed_returns_none(
    patcher,
) -> None:
    table = AuthUsersTableStub()
    patcher.setattr(auth_services, "auth_table", table)

    err = ClientError(
        error_response={"Error": {"Code": "ConditionalCheckFailedException"}},
        operation_name="PutItem",
    )
    table._put_item_side_effect = err

    assert auth_services.create_auth_user("bob", "hash") is None


def test_create_auth_user_other_client_error_raises(patcher) -> None:
    table = AuthUsersTableStub()
    patcher.setattr(auth_services, "auth_table", table)

    err = ClientError(
        error_response={"Error": {"Code": "SomeOtherError"}},
        operation_name="PutItem",
    )
    table._put_item_side_effect = err

    with pytest.raises(ClientError):
        auth_services.create_auth_user("bob", "hash")

