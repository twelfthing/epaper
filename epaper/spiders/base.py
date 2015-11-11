# -*- coding: utf-8 -*-
from urlparse import urljoin
from datetime import datetime

from scrapy import signals
from scrapy.selector import Selector
from scrapy.spiders.crawl import CrawlSpider
from scrapy.xlib.pydispatch import dispatcher

from epaper.items import PaperItem, PageItem

class EpaperSpider(CrawlSpider):

    publish_date = datetime.today() 

    coords = {}

    # def __init__(self):
    #     super(EpaperSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    # def spider_closed(self):
    #     return

    def parse_start_url(self, response):
        reqs = self.parse_page(response)
        paper = PaperItem()
        paper['name'] = self.name.decode('utf-8')
        paper['publish_date'] = self.publish_date.strftime('%Y-%m-%d')
        paper['url'] = response.url
        paper['image'] = [req['image'] for req in reqs if isinstance(req,PageItem) and 'image' in req][0]
        reqs.append(paper)
        for e in reqs:
            yield e

    def _set_coords(self,response, selector):
        for a in selector.xpath('//area'):
            href = a.xpath('@href').extract()[0].strip()
            self.coords[urljoin(response.url,href)] = a.xpath('@coords').extract()[0]


    # def _get_coord_from_area(self, response, selector):
    #     if not selector:
    #         selector = Selector(response)
    #     for a in selector.xpath('//area'):
    #         href = a.xpath('@href').extract()[0].strip()
    #         coords = a.xpath('@coords').extract()[0]
    #         if response.url == urljoin(response.url, href):
    #             return coords
                