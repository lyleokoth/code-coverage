# -*- coding: utf-8 -*-
"""This module contains the database models used by the default blueprint."""
from dataclasses import dataclass

from ..extensions import db
from .constants import EMAIL_MAX_LENGTH


@dataclass
class User(db.Model):
    """A class that represents a user.

    Attributes
    ----------
    id: int
        The unique user identifier
    email: str
        The user's email
    active: bool
        Has the user activated their account

    """

    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(EMAIL_MAX_LENGTH), unique=True, nullable=False)
    active: bool = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email: str) -> None:
        """Create a new user.

        Creates a new user in the user table with an increasing id, with active
        set as True by default and with the given email.

        Attributes
        ----------
        email: str
            The user's email
        """
        self.email = email

    def get_user(self) -> dict:
        """Get user data."""
        user = dict(id=self.id, email=self.email)
        return user
