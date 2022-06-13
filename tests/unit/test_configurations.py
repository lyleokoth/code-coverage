# -*- coding: utf-8 -*-
"""This module tests the different application configurations."""


def test_test_configuration(create_test_app):
    """Test the test configuration."""
    assert create_test_app.config['SECRET_KEY'] == 'supersecretkey'
    assert create_test_app.config['DEBUG'] is True
    assert create_test_app.config['TESTING'] is True

    assert create_test_app.config['POSTGRES_HOST'] == 'localhost'
    assert create_test_app.config['POSTGRES_PORT'] == '5432'
    assert create_test_app.config['POSTGRES_USER'] == 'postgres'
    assert create_test_app.config['POSTGRES_PASSWORD'] == 'mechatronics'
    assert create_test_app.config['POSTGRES_DB'] == 'lyle_test'

    db_conn_string = 'postgresql://postgres:mechatronics@localhost:5432/lyle_test'
    assert create_test_app.config['SQLALCHEMY_DATABASE_URI'] == db_conn_string
    assert create_test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_development_configuration(create_development_app):
    """Test the development configuration."""
    assert create_development_app.config['SECRET_KEY'] == 'supersecretkey'
    assert create_development_app.config['DEBUG'] is True
    assert create_development_app.config['TESTING'] is False

    assert create_development_app.config['POSTGRES_HOST'] == 'localhost'
    assert create_development_app.config['POSTGRES_PORT'] == '5432'
    assert create_development_app.config['POSTGRES_USER'] == 'postgres'
    assert create_development_app.config['POSTGRES_PASSWORD'] == 'mechatronics'
    assert create_development_app.config['POSTGRES_DB'] == 'lyle_dev'

    db_conn_string = 'postgresql://postgres:mechatronics@localhost:5432/lyle_dev'
    assert create_development_app.config['SQLALCHEMY_DATABASE_URI'] == db_conn_string
    assert create_development_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_staging_configuration(create_staging_app):
    """Test the staging configuration."""
    assert create_staging_app.config['SECRET_KEY'] == 'supersecretkey'
    assert create_staging_app.config['DEBUG'] is False
    assert create_staging_app.config['TESTING'] is False

    assert create_staging_app.config['POSTGRES_HOST'] == 'localhost'
    assert create_staging_app.config['POSTGRES_PORT'] == '5432'
    assert create_staging_app.config['POSTGRES_USER'] == 'postgres'
    assert create_staging_app.config['POSTGRES_PASSWORD'] == 'mechatronics'
    assert create_staging_app.config['POSTGRES_DB'] == 'lyle_stage'

    db_conn_string = 'postgresql://postgres:mechatronics@localhost:5432/lyle_stage'
    assert create_staging_app.config['SQLALCHEMY_DATABASE_URI'] == db_conn_string
    assert create_staging_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_production_configuration(create_production_app):
    """Test the production configuration."""
    assert create_production_app.config['SECRET_KEY'] == 'supersecretkey'
    assert create_production_app.config['DEBUG'] is False
    assert create_production_app.config['TESTING'] is False

    assert create_production_app.config['POSTGRES_HOST'] == 'localhost'
    assert create_production_app.config['POSTGRES_PORT'] == '5432'
    assert create_production_app.config['POSTGRES_USER'] == 'postgres'
    assert create_production_app.config['POSTGRES_PASSWORD'] == 'mechatronics'
    assert create_production_app.config['POSTGRES_DB'] == 'lyle_prod'

    db_conn_string = 'postgresql://postgres:mechatronics@localhost:5432/lyle_prod'
    assert create_production_app.config['SQLALCHEMY_DATABASE_URI'] == db_conn_string
    assert create_production_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
