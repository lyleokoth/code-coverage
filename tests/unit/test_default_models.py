# -*- coding: utf-8 -*-
"""This module tests the models used by the default blueprint i.e api/blueprints/default/models."""
from sqlalchemy import true

from api.blueprints.default.models import User


def test_user():
    """Test that the user is created correctly."""
    user_email = 'lyle@gmail.com'
    user = User(email=user_email)

    assert isinstance(user.email, str)
    assert user.email == user_email
