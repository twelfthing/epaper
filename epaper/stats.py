#coding=utf-8

"""
    Author: ChengCheng
    Date  : 2015-12-20
"""

import json
import redis
from scrapy.statscollectors import MemoryStatsCollector

red = redis.Redis()

class RealTimeStatsCollector(MemoryStatsCollector):

    def __init__(self, crawler):
        super(RealTimeStatsCollector, self).__init__(crawler)

    def set_value(self, key, value, spider=None):
        self._stats[key] = value
        self._stats['start_time'] = ''
        self._stats['finish_time'] = ''
        print json.dumps(self._stats)
        red.publish('spider.stats', json.dumps(self._stats))

    def set_stats(self, stats, spider=None):
        self._stats = stats

    def inc_value(self, key, count=1, start=0, spider=None):
        d = self._stats
        d[key] = d.setdefault(key, start) + count

    def clear_stats(self, spider=None):
        self._stats.clear()
