# -*- coding: utf-8 -*-
"""This module tests the helper methods in api.blueprints.default.helpers module."""
import pytest

from api.blueprints.default.helpers import (
    check_if_user_exists,
    check_if_user_exists_with_id,
    create_new_user,
    is_email_address_format_valid,
)


def test_check_if_user_exists_with_id_empty_id():
    """Test if the function raises ValueError with an empty id."""
    with pytest.raises(ValueError):
        check_if_user_exists_with_id(None)


def test_check_if_user_exists_with_id_string_id():
    """Test if the function raises ValueError with a string id."""
    with pytest.raises(ValueError):
        check_if_user_exists_with_id('')


def test_check_if_user_exists_with_id(client, create_app):
    """Test if the function returns True for an existing user."""
    resp = client.post('/user', json = {"email": "lyle@gmail.com"})  # noqa: E251
    assert resp.status_code == 201
    with create_app.app_context():
        user_exists = check_if_user_exists_with_id(resp.json['id'])
        assert user_exists is True


def test_check_if_user_exists_with_id_non_existent_user(client, create_app):  # pylint: disable=W0613
    """Test if the function returns False for a non-existing user."""
    with create_app.app_context():
        user_exists = check_if_user_exists_with_id(1)
        assert user_exists is False


def test_check_if_user_exists_empty_id():
    """Test if the function raises ValueError with an empty id."""
    with pytest.raises(ValueError):
        check_if_user_exists(None)


def test_check_if_user_exists_string_id():
    """Test if the function raises ValueError with a string id."""
    with pytest.raises(ValueError):
        check_if_user_exists('')


def test_check_if_user_exists(client, create_app):
    """Test if the function returns True for an existing user."""
    resp = client.post('/user', json={"email": "lyle@gmail.com"})
    assert resp.status_code == 201
    with create_app.app_context():
        user_exists = check_if_user_exists(resp.json['email'])
        assert user_exists is True


def test_check_if_user_exists_non_existent_user(create_app):
    """Test if the function returns False for a non-existing user."""
    with create_app.app_context():
        user_exists = check_if_user_exists("dummy@gmail.com")
        assert user_exists is False


def test_is_email_address_format_valid_empty_email():
    """Test that the function raises ValueError on empty email."""
    with pytest.raises(ValueError):
        is_email_address_format_valid('')


def test_is_email_address_format_valid_non_string_email():
    """Test that the function raises ValueError on a non-string email."""
    with pytest.raises(ValueError):
        is_email_address_format_valid(20)


def test_is_email_address_format_valid_invalid_email():
    """Test that the function returns False on invalid email."""
    invalid_email = 'lyle-the-desiger'
    valid_email = is_email_address_format_valid(invalid_email)
    assert valid_email is False


def test_create_new_user(create_app, create_db):
    """Test that a new user is created when correct data is supplied."""
    user_email = 'lyle@gmail.com'
    user_data = dict(email=user_email)
    with create_app.app_context():
        create_db.drop_all()
        create_db.create_all()
        created_user = create_new_user(user_data=user_data)
        assert created_user['email'] == user_email
