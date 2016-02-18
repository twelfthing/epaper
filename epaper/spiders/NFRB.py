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

class NFRBSpider(EpaperSpider):

    name = 'NFRB-GZ'

    zh_name = u'南方日报'

    publish_date = datetime.today() 

    base_url = 'http://epaper.southcn.com/nfdaily/html/%s' % publish_date.strftime('%Y-%m/%d')

    start_urls = ['%s/node_2.htm' % base_url,]
    rules = (
        Rule(
            LinkExtractor(allow=('%s/node_\d+\.htm' % base_url),
            deny=('%s/node_1\.htm' % base_url)),
            'parse_page',
            follow = True,
        ),
    )

    def parse_start_url(self, response):
        reqs = self.parse_page(response)
        x = Selector(response)
        paper = PaperItem()
        paper['name'] = self.name.decode('utf-8')
        paper['publish_date'] = self.publish_date.strftime('%Y-%m-%d')
        paper['url'] = response.url
        paper['image'] = reqs[0]['image']
        reqs.append(paper)
        for e in reqs:
            yield e

    def parse_page(self, response):
        x = Selector(response)
        page = PageItem()
        reqs = []
        page['image'] = {'origin':urljoin(response.url, x.xpath('//img[@usemap="#PagePicMap"]/@src').extract()[0])}
        page['number'] = x.xpath('//div[@class="column epaper"]//h3//text()').extract()[0].strip()[:-1]
        page['name'] = x.xpath('//div[@class="column epaper"]//h3//text()').extract()[1]
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        n = ArticleItem()
        n['leadtitle'] = u''.join(x.xpath('//div[@id="article"]//span[@class="primers"][1]//text()').extract())
        n['title'] = u''.join(x.xpath('//div[@id="article"]//h1//text()').extract())
        n['subtitle'] = u''.join(x.xpath('//div[@id="article"]//span[@class="primers"][2]//text()').extract())
        n['author'] = u''
        n['url'] = response.url
        n['referer'] = response.request.headers.get('Referer',None)
        n['content'] = u'\n'.join(x.xpath('//founder-content//p//text()').extract())
        areas = x.xpath('//area')
        for a in areas:
            href = a.xpath('@href').extract()[0].strip()
            coords = a.xpath('@coords').extract()[0]
            if n['url'] == urljoin(response.url, href):
                n['coords'] = coords
                break
        image_links = x.xpath('//table[@width="400"]//img//@src').extract()
        #image_descs = x.xpath('//table[@width="400"]//img/../../../tr[2]//text()').extract()
        n['images'] = [{'origin':urljoin(response.url,im)} for im in image_links]  
        return [n]


