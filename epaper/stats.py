#coding=utf-8

"""
    Author: ChengCheng
    Date  : 2015-12-20
"""

import json
import redis
import datetime
from scrapy.statscollectors import MemoryStatsCollector

red = redis.Redis()

class RealTimeStatsCollector(MemoryStatsCollector):

    def __init__(self, crawler):
        super(RealTimeStatsCollector, self).__init__(crawler)

    def set_value(self, key, value, spider=None):
        self._stats[key] = value
        if 'start_time' in self._stats and isinstance(self._stats['start_time'], datetime.datetime):
            self._stats['start_time'] = self._stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')
        if 'finish_time' in self._stats and isinstance(self._stats['finish_time'], datetime.datetime):
            self._stats['finish_time'] = self._stats['finish_time'].strftime('%Y-%m-%d %H:%M:%S')


        djson = {'name': self.spider_name, 'data':self._stats}
        red.publish('spider.stats', json.dumps(djson))

    def set_stats(self, stats, spider=None):
        self._stats = stats

    def inc_value(self, key, count=1, start=0, spider=None):
        d = self._stats
        d[key] = d.setdefault(key, start) + count

    def clear_stats(self, spider=None):
        self._stats.clear()

    def open_spider(self, spider):
        self.spider_name = spider.name