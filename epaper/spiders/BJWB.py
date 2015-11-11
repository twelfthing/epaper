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

class BJWBSpider(EpaperSpider):

    name = '北京晚报'

    publish_date = datetime.today() 
    
    base_url = 'http://bjwb.bjd.com.cn/html/%s' % publish_date.strftime('%Y-%m/%d')

    start_urls = ['%s/node_82.htm' % base_url,]

    rules = (
        Rule(
            LinkExtractor(allow=('%s/node_\d+\.htm' % base_url)),
            'parse_page',
            follow = True,
        ),
    )


    def parse_page(self, response):
        x = Selector(response)
        reqs = []
        page = PageItem()
        page['image'] = {'origin':urljoin(response.url, x.xpath('//img[@usemap="#PagePicMap"]/@src').extract()[0])}
        page['number'],page['name'] = ''.join(x.xpath('//td[@width="145"]//text()').extract()).strip().split(u'：')
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        self._set_coords(response, x)
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        n = ArticleItem()
        n['leadtitle'] = u''.join(x.xpath('//td[@class="font01"]/../../tr[1]//text()').extract()).strip()
        n['title'] = u''.join(x.xpath('//td[@class="font01"]/strong/text()').extract()).strip()
        n['subtitle'] = u''.join(x.xpath('//td[@class="font01"]/../../tr[3]//text()').extract()).strip()
        n['author'] = u''.join(x.xpath('//td[@class="font01"]/../../tr[4]//text()').extract()).strip()
        n['url'] = response.url
        n['referer'] = response.request.headers.get('Referer',None)
        n['content'] = u'\n'.join(x.xpath('//div[@id="ozoom"]//p/text()').extract())
        n['coords'] = self.coords[response.url]
        n['images'] = [{'origin':im} for im in x.xpath('//table[@width="315"]//img/@src').extract()]
        
        return n



