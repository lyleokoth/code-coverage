# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
import os

from sqlalchemy_utils import database_exists

from .blueprints.extensions import app_logger


def set_flask_environment(app) -> str:
    """Set the flask development environment.

    Parameters
    ----------
    app: flask.Flask
        The flask application object

    Raises
    ------
    KeyError
        If the FLASK_ENV environment variable is not set.

    Returns
    -------
    str:
        Flask operating environment i.e development

    """
    try:
        if os.environ['FLASK_ENV'] == 'production':  # pragma: no cover
            app.config.from_object('api.config.ProductionConfig')
            app_logger.info('The FLASK_ENV is set to production. Using the production config.')
        elif os.environ['FLASK_ENV'] == 'development':  # pragma: no cover
            app.config.from_object('api.config.DevelopmentConfig')
            app_logger.info('The FLASK_ENV is set to development. Using the development config.')
        elif os.environ['FLASK_ENV'] == 'test':
            app.config.from_object('api.config.TestingConfig')
            app_logger.info('The FLASK_ENV is set to test. Using the test config.')
        elif os.environ['FLASK_ENV'] == 'stage':
            app.config.from_object('api.config.StagingConfig')
            app_logger.info('The FLASK_ENV is set to stage. Using the stage config.')
    except KeyError:
        app.config.from_object('api.config.DevelopmentConfig')
        app_logger.warning('The FLASK_ENV is not set. Using development.')
        return 'development'

    return os.environ['FLASK_ENV']


def create_db_conn_string(flask_env: str) -> str:
    """Create the database connection string.

    Creates the database connection string for a given flask environment.

    Attributes
    ----------
    flask_env: str
        The Flask environment.

    Raises
    ------
    ValueError:
        If the flask_env is empty, is not a string or is any value apart from
        test, development, stage or production.

    Returns
    -------
    db_connection_string: str
        The database connection string
    """
    if not flask_env:
        app_logger.exception('When creating the database connection string, the FLASK_ENV is not set.')
        raise ValueError('The flask_env cannot be a null value.')

    if not isinstance(flask_env, str):
        app_logger.exception('When creating the database connection string,tThe FLASK_ENV is not a string.')
        raise ValueError('The flask_env has to be string')

    if flask_env not in ['development', 'test', 'stage', 'production']:
        msg = 'When creating database connection string, FLASK_ENV is not in test, development, stage or production.'
        app_logger.exception(msg)
        raise ValueError('The flask_env has to be test, development, stage or production.')

    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_DB = os.environ['POSTGRES_DB']

    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def check_if_database_exists(db_connection_string: str) -> bool:
    """Check if database exists.

    Ensures that the database exists before starting the application.

    Attributes
    ----------
    db_connection: str
        The database URL

    Raises
    ------
    ValueError:
        If the db_connection_string is empty or is not a string.

    Returns
    -------
    db_exists: bool
        True if database exists or False if it does not
    """
    if not db_connection_string:
        app_logger.exception('When checking if the database exists, the database connection string is not set.')
        raise ValueError('The db_connection_string cannot be a null value.')

    if not isinstance(db_connection_string, str):
        app_logger.exception('When checking if the database exists, the database connection string is not a string.')
        raise ValueError('The db_connection_string has to be string')

    db_exists = database_exists(db_connection_string)

    return db_exists


def are_environment_variables_set() -> bool:  # pylint: disable=R0911, R0915
    """Check if all the environment variables are set.

    Raises
    ------
    KeyError
        If any of the environment variables are not set.

    Returns
    -------
    bool:
        True if all the environment variables are set else False if any is missing.

    """
    try:
        os.environ['FLASK_APP']  # pylint: disable=W0104
        app_logger.info(f"The FLASK_APP is set to {os.environ['FLASK_APP']}")
    except KeyError:
        app_logger.exception('The FLASK_APP is not set')
        return False

    try:
        os.environ['FLASK_ENV']  # pylint: disable=W0104
        app_logger.info(f"The FLASK_ENV is set to {os.environ['FLASK_ENV']}")
    except KeyError:
        app_logger.exception('The FLASK_ENV is not set')
        return False

    try:
        os.environ['SECRET_KEY']  # pylint: disable=W0104
        app_logger.info(f"The SECRET_KEY is set to {os.environ['SECRET_KEY']}")
    except KeyError:
        app_logger.exception('The SECRET_KEY is not set')
        return False

    try:
        os.environ['POSTGRES_HOST']  # pylint: disable=W0104
        app_logger.info(f"The POSTGRES_HOST is set to {os.environ['POSTGRES_HOST']}")
    except KeyError:
        app_logger.exception('The POSTGRES_HOST is not set')
        return False

    try:
        os.environ['POSTGRES_DB']  # pylint: disable=W0104
        app_logger.info(f"The POSTGRES_DB is set to {os.environ['POSTGRES_DB']}")
    except KeyError:
        app_logger.exception('The POSTGRES_DB is not set')
        return False

    try:
        os.environ['POSTGRES_PORT']  # pylint: disable=W0104
        app_logger.info(f"The POSTGRES_PORT is set to {os.environ['POSTGRES_PORT']}")
    except KeyError:
        app_logger.exception('The POSTGRES_PORT is not set')
        return False

    try:
        os.environ['POSTGRES_USER']  # pylint: disable=W0104
        app_logger.info(f"The POSTGRES_USER is set to {os.environ['POSTGRES_USER']}")
    except KeyError:
        app_logger.exception('The POSTGRES_USER is not set')
        return False

    try:
        os.environ['POSTGRES_PASSWORD']  # pylint: disable=W0104
        app_logger.info(f"The POSTGRES_PASSWORD is set to {os.environ['POSTGRES_PASSWORD']}")
    except KeyError:
        app_logger.exception('The POSTGRES_PASSWORD is not set')
        return False

    try:
        db_con_str = create_db_conn_string(os.environ['FLASK_ENV'])
        db_exists = check_if_database_exists(db_con_str)

        if db_exists:
            app_logger.info(f'The database {db_con_str} exists.')
            return True

        app_logger.error(f'The database {db_con_str} does not exist.')
        return False

    except ValueError as v:
        app_logger.exception(v)
        app_logger.exception('Unable to verify database existence...')
        return False
