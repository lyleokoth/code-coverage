# -*- coding: utf-8 -*-
"""This module sets up the fixtures that will be used in our testing."""
import pytest

from api import app, db
from api.blueprints.default.models import User
from api.config import DevelopmentConfig, ProductionConfig, StagingConfig, TestingConfig


@pytest.fixture
def create_app():
    """Create the app instance."""
    return app


@pytest.fixture
def create_db():
    """Create the db instance."""
    return db


@pytest.fixture
def client():
    """Create the test client."""
    app.config.from_object(TestingConfig)
    test_client = app.test_client()
    with app.app_context():
        db.drop_all()
        db.create_all()

    return test_client


@pytest.fixture
def create_test_app():
    """Create the test client with the test config."""
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture
def create_development_app():
    """Create the test client with the development config."""
    app.config.from_object(DevelopmentConfig)
    return app


@pytest.fixture
def create_staging_app():
    """Create the test client with the staging config."""
    app.config.from_object(StagingConfig)
    return app


@pytest.fixture
def create_production_app():
    """Create the test client with the production config."""
    app.config.from_object(ProductionConfig)
    return app
