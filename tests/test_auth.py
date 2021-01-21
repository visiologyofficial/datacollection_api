import pytest


def test_auth_by_username(vdatacollection_without_auth):
    vdatacollection_without_auth.auth_by_username(pytest.USERNAME, pytest.PASSWORD)
    assert vdatacollection_without_auth.headers['Authorization']


def test_auth_by_token(vdatacollection_without_auth):
    token = vdatacollection_without_auth.get_token(pytest.USERNAME, pytest.PASSWORD)
    from main import token_type
    vdatacollection_without_auth.auth_by_token(token_type, token)
    from main import headers
    assert headers['Authorization'].split() != token
