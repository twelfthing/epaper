# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
from datetime import datetime

from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor

from epaper.items import PaperItem, PageItem, ArticleItem
from epaper.spiders.base import EpaperSpider

class HBRBSpider(EpaperSpider):

    name = 'HBRB-HB'

    zh_name = u'湖北日报'

    publish_date = datetime.today() 

    base_url = 'http://ctdsb.cnhubei.com/HTML/hbrb/%s' % publish_date.strftime('%Y%m%d')

    start_urls = ['%s/hbrb1.html' % base_url,]
    
    rules = (
        Rule(
            LinkExtractor(allow=('%s/hbrb\d+.html' % base_url),),
            'parse_page',
            follow = True,
        ),
    )

    def parse_page(self, response):
        x = Selector(response)
        reqs = []
        page = PageItem()
        page['image'] = {'origin':urljoin(response.url, x.xpath('//img[@usemap="#FPMap0"]/@src').extract()[0])}
        page['number'], page['name'] = ''.join(x.xpath('//td[@bgcolor="#004D95"]/span[@class="STYLE1"]/text()').extract()).split()
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        self._set_coords(response, x)
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        n = ArticleItem()
        n['leadtitle'] = u''.join(x.xpath('//table[@id="Table17"]/tr[0]//text()').extract()).strip()
        n['title'] = u''.join(x.xpath('//table[@id="Table17"]/tr[1]//text()').extract()).strip()
        n['subtitle'] = u''.join(x.xpath('//table[@id="Table17"]/tr[3]//text()').extract()).strip()
        n['url'] = response.url
        n['referer'] = response.request.headers.get('Referer',None)
        n['content'] = u'\n'.join(x.xpath('//div[@id="copytext"]/font/text()').extract())
        n['coords'] = self.coords[response.url]
        n['images'] = [{'origin':im} for im in x.xpath('//div[@id="copytext"]//img/@src').extract()]
        
        return n

