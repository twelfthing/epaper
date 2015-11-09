# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.spiders import Spider
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class EpaperSpider(Spider):

    publish_date = datetime.today() 

    # def __init__(self):
    #     super(EpaperSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    # def spider_closed(self):
    #     return
