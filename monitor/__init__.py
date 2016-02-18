#coding=utf-8

"""
    Author: ChengCheng
    Date  : 2016-01-20
"""
import settings
from logging.config import dictConfig

def setup():
    # 全局的日志配置 
    dictConfig(settings.LOG_CONFIG)


__all__ = ('setup',)