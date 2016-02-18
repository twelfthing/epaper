#coding=utf-8

"""
    Author: ChengCheng
    Date  : 2016-01-20
"""

import settings

def _get_redis_db():
    import redis
    return redis.Redis()


def _get_mongo_connection():
    import pymongo
    connection = pymongo.MongoClient(
        settings.MONGODB_SERVER, settings.MONGODB_PORT, connectTimeoutMS=50000)
    db = connection[settings.MONGODB_DB]
    db.authenticate(settings.MONGODB_USER, settings.MONGODB_PASSWORD)
    return db
