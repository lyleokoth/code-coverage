# -*- coding: utf-8 -*-
"""This module declares the error handlers."""


def handle_bad_request(e):
    """Handle all Bad Request errors."""
    print(e)
    return 'The user data provided is badly formatted. Check the JSON!', 400
