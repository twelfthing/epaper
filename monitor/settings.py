# coding=utf-8

"""
    Author: ChengCheng
    Date  : 2015-12-20
"""
import os
import logging
from logging.config import dictConfig


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
settings = {}


def log_config():
    dict_conf = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s',
            },
        },
        'handlers': {
            'file_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(PROJECT_ROOT, '..', 'log', 'monitor.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 365 * 10,
                'formatter': 'standard',
            },
        },
        'loggers': {
            'web': {
                'handlers': ['file_handler'],
                'level': 'DEBUG',
            },
        }
    }
    dictConfig(dict_conf)

log_config()