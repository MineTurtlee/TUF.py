import pytest

from tuf.errors import AuthenticationError, APIError, SyntaxError, ConflictingArgs


def test_authentication_error_message():
    err = AuthenticationError("user1", "bad password")
    assert "Authentication failed for user1" in str(err)


def test_api_error_message():
    err = APIError("/path", "server error")
    assert "/path" in str(err) and "server error" in str(err)


def test_syntax_error_message():
    err = SyntaxError("id", "name")
    msg = str(err)
    assert "id, name" in msg and "were not passed correctly" in msg


def test_conflicting_args_message():
    err = ConflictingArgs("id", "name")
    assert "conflicting args" in str(err)
