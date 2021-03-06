# -*- coding: utf-8 -*-

import os

os_env = os.environ
import sys
import binascii

sys.path.append('..')
from common import common_file


class Config(object):
    if os.path.exists('/poestat/key/web_secret_key.txt'):
        pass
    else:
        common_file.com_file_save_data('/poestat/key/web_secret_key.txt',
                                       binascii.hexlify(os.urandom(24)).decode(), False)
    SECRET_KEY = os_env.get('WEB_SECRET',
                            common_file.com_file_load_data('/poestat/key/web_secret_key.txt',
                                                           False))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + os.environ['POSTGRES_USER'] + ":" \
                              + os.environ['POSTGRES_PASSWORD'] + "@poepgbounce:6432/" \
                              + os.environ['POSTGRES_DB']
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
