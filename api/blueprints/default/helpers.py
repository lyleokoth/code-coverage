# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import re

from ..extensions import db
from .constants import EMAIL_MAX_LENGTH, EMAIL_MIN_LENGTH
from .exceptions import (
    EmailAddressTooLong,
    EmptyUserData,
    InvalidEmailAddressFormat,
    MissingEmailData,
    MissingEmailKey,
    NonDictionaryUserData,
    UserDoesNotExists,
    UserExists,
)
from .models import User


def check_if_user_exists_with_id(user_id: int) -> bool:
    """Check if the user with the given user_id exists."""
    if not user_id:
        raise ValueError('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer')

    user = User.query.filter_by(id=user_id).first()

    if user:
        return True

    return False


def check_if_user_exists(user_email: str) -> bool:
    """Check if the user with the given user_email exists."""
    if not user_email:
        raise ValueError('The user_email has to be provided.')

    if not isinstance(user_email, str):
        raise ValueError('The user_email has to be an integer')

    user = User.query.filter_by(email=user_email).first()

    if user:
        return True

    return False


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError('The email_address cannot be an empty value')

    if not isinstance(email_address, str):
        raise ValueError('The email_address must be a string')

    #  Regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email_address):
        return True

    return False


def create_new_user(user_data: dict) -> dict:
    """Create a new user."""
    if not user_data:
        raise EmptyUserData('The user data cannot be empty.')

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData('user_data must be a dict')

    if 'email' not in user_data.keys():
        raise MissingEmailKey('The email is missing from the user data')

    if not user_data['email']:
        raise MissingEmailData('The email data is missing')

    if len(user_data['email']) > EMAIL_MAX_LENGTH:
        raise EmailAddressTooLong(f'The email address should be less than {EMAIL_MAX_LENGTH} characters!')

    if not is_email_address_format_valid(user_data['email']):
        raise InvalidEmailAddressFormat('The email address is invalid')

    if check_if_user_exists(user_data['email']):
        raise UserExists(f'The email adress {user_data["email"]} is already in use.')

    user = User(email=user_data['email'])
    db.session.add(user)
    db.session.commit()

    return user.get_user()


def handle_create_user(request_data: dict):  # pylint: disable=R0911
    """Handle the POST request to the /user route."""
    try:
        new_user = create_new_user(request_data)
    except EmptyUserData as e:
        print(e)
        return str(e), 400
    except NonDictionaryUserData as e:
        print(e)
        return str(e), 400
    except MissingEmailKey as e:
        print(e)
        return str(e), 400
    except EmailAddressTooLong as e:
        print(e)
        return str(e), 400
    except InvalidEmailAddressFormat as e:
        print(e)
        return str(e), 400
    except UserExists as e:
        print(e)
        return str(e), 400
    except MissingEmailData as e:
        print(e)
        return str(e), 400
    else:
        return new_user, 201


def get_user(user_id: int) -> dict:
    """Get the user with the given id."""
    if not user_id:
        raise EmptyUserData('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer.')

    if not check_if_user_exists_with_id(user_id):
        raise UserDoesNotExists(f'The user with id {user_id} does not exist.')

    user = User.query.filter_by(id=user_id).first()

    return user.get_user()


def handle_get_user(user_id: int):
    """Handle the GET request to the /user route."""
    try:
        user = get_user(user_id)
    except UserDoesNotExists as e:
        print(e)
        return str(e), 404
    except EmptyUserData as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        return str(e), 400
    else:
        return user, 200


def delete_user(user_id: int) -> dict:
    """Delete the user with the given id."""
    if not user_id:
        raise EmptyUserData('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer.')

    if not check_if_user_exists_with_id(user_id):
        raise UserDoesNotExists(f'The user with id {user_id} does not exist.')

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return user.get_user()


def handle_delete_user(user_id: int):
    """Handle the DELETE request to the /user route."""
    try:
        user = delete_user(user_id)
    except UserDoesNotExists as e:
        print(e)
        return str(e), 404
    except EmptyUserData as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        return str(e), 400
    else:
        return user, 200


def update_user(user_id: int, user_data: dict) -> dict:
    """Update the user with the given id."""
    if not user_id:
        raise EmptyUserData('The user_id has to be provided.')

    if not isinstance(user_id, int):
        raise ValueError('The user_id has to be an integer.')

    if not check_if_user_exists_with_id(user_id):
        raise UserDoesNotExists(f'The user with id {user_id} does not exist.')

    if not user_data:
        raise EmptyUserData('The user data cannot be empty.')

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData('user_data must be a dict')

    if 'email' not in user_data.keys():
        raise MissingEmailKey('The email is missing from the user data')

    if not user_data['email']:
        raise MissingEmailData('The email data is missing')

    if len(user_data['email']) > 120:
        raise EmailAddressTooLong('The email address is too long')

    if not is_email_address_format_valid(user_data['email']):
        raise InvalidEmailAddressFormat('The email address is invalid')

    if check_if_user_exists(user_data['email']):
        raise UserExists(f'The email adress {user_data["email"]} is already in use.')

    user = User.query.filter_by(id=user_id).first()
    user.email = user_data['email']
    db.session.commit()

    return user.get_user()


def handle_update_user(user_id: int, user_data: dict):  # pylint: disable=R0911
    """Handle the GET request to the /user route."""
    try:
        user = update_user(user_id, user_data)
    except UserDoesNotExists as e:
        print(e)
        return str(e), 404
    except EmptyUserData as e:
        print(e)
        return str(e), 400
    except ValueError as e:
        print(e)
        return str(e), 400
    except NonDictionaryUserData as e:
        print(e)
        return str(e), 400
    except MissingEmailKey as e:
        print(e)
        return str(e), 400
    except EmailAddressTooLong as e:
        print(e)
        return str(e), 400
    except InvalidEmailAddressFormat as e:
        print(e)
        return str(e), 400
    except UserExists as e:
        print(e)
        return str(e), 400
    except MissingEmailData as e:
        print(e)
        return str(e), 400
    else:
        return user, 200
