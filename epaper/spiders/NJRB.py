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

class NJRBSpider(EpaperSpider):

    name = 'NJRB-NJ'

    zh_name = u'南京日报'

    publish_date = datetime.today() 
    
    base_url = 'http://njrb.njdaily.cn/njrb/html/%s' % publish_date.strftime('%Y-%m/%d')

    start_urls = ['%s/node_3.htm' % base_url,]

    rules = (
        Rule(
            LinkExtractor(allow=('%s/node_\d+\.htm' % base_url) ),
            'parse_page',
            follow = True,
        ),
    )

    def parse_page(self, response):
        x = Selector(response)
        reqs = []
        page = PageItem()
        page['image'] = {'origin':urljoin(response.url, x.xpath('//div[@class="pagepic"]//img/@src').extract()[0])}
        page['number'] = u''.join(x.xpath('//div[@class="pagename_left"]/text()').extract()).replace(u'：','').strip()
        page['name'] = u''.join(x.xpath('//div[@class="pagename_left"]/strong/text()').extract()).strip()
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        self._set_coords(response, x)
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        n = ArticleItem()
        article_select = x.xpath('//div[@class="title"]')
        n['leadtitle'] = u''.join(article_select.xpath('div[1]/text()').extract())
        n['title'] = u''.join(article_select.xpath('div[@class="title1"]/text()').extract())
        n['subtitle'] = u''.join(article_select.xpath('div[3]/text()').extract())
        n['author'] = u''.join(article_select.xpath('div[4]/text()').extract())
        n['url'] = response.url
        n['referer'] = response.request.headers.get('Referer',None)
        n['content'] = u'\n'.join(x.xpath('//div[@class="content_tt"]//text()').extract()).strip()
        n['coords'] = self.coords[response.url]
        n['images'] = [{'origin':im} for im in x.xpath('//div[@class="content"]//img/@src').extract()]

        return n

