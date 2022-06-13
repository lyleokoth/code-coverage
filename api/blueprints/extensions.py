# -*- coding: utf-8 -*-
"""This module creates the flask extensions that we will use."""
import logging
import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_logger():
    """Create the application logger."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
    LOG_FILE = os.getenv('LOG_FILE_PATH') or os.path.join(BASE_DIR, 'app.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    flask_env = os.getenv('FLASK_ENV', 'development')

    if flask_env == 'development':
        logger.addHandler(stream_handler)

    return logger


app_logger = create_logger()
