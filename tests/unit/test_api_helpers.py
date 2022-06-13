# -*- coding: utf-8 -*-
"""This module tests the helper methods in api.helpers module."""
import os
from unittest import mock

import pytest

from api.helpers import (
    are_environment_variables_set,
    check_if_database_exists,
    create_db_conn_string,
    set_flask_environment,
)


@mock.patch.dict(os.environ, {"FLASK_ENV": "test"})
def test_set_flask_environment_env_is_test(create_app):
    """Test that the test environment is created when FLASK_ENV is set to test."""
    flask_env = set_flask_environment(create_app)
    assert flask_env == 'test'


@mock.patch.dict(os.environ, clear=True)
def test_set_flask_environment_env_not_set(create_app):
    """Test that the development environment is created when FLASK_ENV is not set."""
    flask_env = set_flask_environment(create_app)
    assert flask_env == 'development'


def test_create_db_conn_string_valid():
    """Test that a valid flask_env creates a string."""
    db_conn_str = create_db_conn_string('development')
    db_conn_string = 'postgresql://postgres:mechatronics@localhost:5432/lyle_dev'
    assert isinstance(db_conn_str, str)
    assert db_conn_str == db_conn_string


def test_create_db_conn_string_empty_str():
    """Test that an empty flask_env raises a valueError."""
    with pytest.raises(ValueError):
        create_db_conn_string('')


def test_create_db_conn_string_int_value():
    """Test that an integer value for flask_env raises a valueError."""
    with pytest.raises(ValueError):
        create_db_conn_string(10)


def test_create_db_conn_string_invalid_option():
    """Test that an invalid value flask_env raises a valueError.

    The flask_env value has to be test, development, stage or production.
    """
    with pytest.raises(ValueError):
        create_db_conn_string('prod')


def test_check_if_database_exists(create_test_app):
    """Check if we get a True value for an existing database.

    The client fixture runs only if the database was created. The create_test_app
    fixture gives us access to the test database url.
    """
    test_db_url = create_test_app.config['SQLALCHEMY_DATABASE_URI']
    db_exists = check_if_database_exists(test_db_url)
    assert db_exists is True


def test_check_if_database_exists_non_xsistant_db():
    """Check if we get a False value for a non existing database."""
    test_db_url = 'postgresql://postgres:mechatronics@localhost:5432/no-existant-db'
    db_exists = check_if_database_exists(test_db_url)
    assert db_exists is False


def test_check_if_database_exists_empty_db_url():
    """Check if the function raises ValueError for an empty connection string."""
    with pytest.raises(ValueError):
        check_if_database_exists('')


def test_check_if_database_exists_non_string_url():
    """Check if the function raises ValueError for a non-string connection string."""
    with pytest.raises(ValueError):
        check_if_database_exists(10)


def test_are_environment_variables_set():
    """Test if we get True when the Env variables are set.

    Since the environment variables are currently set, they are loaded when
    the app is created and we are loading the app, we should get a True value.
    """
    are_env_set = are_environment_variables_set()
    assert are_env_set is True


@mock.patch.dict(os.environ, clear=True)
def test_are_flask_environment_variable_set_env_not_set():
    """Test if we get False when the Env variables are not set."""
    are_env_set = are_environment_variables_set()
    assert are_env_set is False


@mock.patch.dict(os.environ, {"FLASK_APP": "api/__init__.py"}, clear=True)
def test_are_environment_variables_set_only_FLASK_APP_set():
    """Test if we get False when the Env variables are not set."""
    are_env_set = are_environment_variables_set()
    assert are_env_set is False
