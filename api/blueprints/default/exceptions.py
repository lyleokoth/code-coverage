# -*- coding: utf-8 -*-
"""This module has exceptions that are used in the other modules in this package."""


class EmptyUserData(Exception):
    """Raised when no user data is provided."""


class NonDictionaryUserData(Exception):
    """Raised when the user data is not provided in a dictionary."""


class MissingEmailKey(Exception):
    """Raised when the 'email' key is missing in user data."""


class MissingEmailData(Exception):
    """Raised when the email is empty in user data."""


class EmailAddressTooLong(Exception):
    """Raised when the provided email address is too long."""


class InvalidEmailAddressFormat(Exception):
    """Raised when the email address format is invalid."""


class UserExists(Exception):
    """Raised when the given user exists."""


class UserDoesNotExists(Exception):
    """Raised when the given user does not exist."""
