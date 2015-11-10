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

class WHWBSpider(EpaperSpider):

    name = '武汉晚报'

    publish_date = datetime.today() 
    
    base_url = 'http://whwb.cjn.cn/html/%s' % publish_date.strftime('%Y-%m/%d')

    start_urls = ['%s/node_22.htm' % base_url,]

    rules = (
        Rule(
            LinkExtractor(allow=('%s/node_\d+\.htm' % base_url)),
            'parse_page',
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
        page['number'],page['name'] = ''.join(x.xpath('//td[@width="145"]//text()').extract()).split(u'：')
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        article = ArticleItem()
        article['leadtitle'] = u''.join(x.xpath('//table[@width="98%"]//td[@class="bt2"]/../../tr[1]//td//text()').extract())
        article['title'] = u''.join(x.xpath('//td[@class="bt1"]//text()').extract())
        article['subtitle'] = u''.join(x.xpath('//table[@width="98%"]//td[@class="bt2"]/../../tr[2]//td//text()').extract())
        article['author'] = u''.join(x.xpath('//table[@width="98%"]//td[@class="bt2"]/../../tr[3]//td//text()').extract())
        article['url'] = response.url
        article['referer'] = response.request.headers.get('Referer',None)
        article['content'] = u'\n'.join(x.xpath('//div[@id="ozoom"]//p/text()').extract())
        areas = x.xpath('//area')
        for a in areas:
            href = a.xpath('@href').extract()[0].strip()
            coords = a.xpath('@coords').extract()[0]
            if article['url'] == urljoin(response.url, href):
                article['coords'] = coords
                break
        image_links = x.xpath('//td[@class="font6"]//img//@src').extract()
        image_descs = [''.join(i.xpath('text()').extract()) for i in x.xpath('//td[@class="font6"]//img/../p')]
        article['images'] = [{'origin':urljoin(response.url,im[0]), 'desc':im[1]} for im in zip(image_links,image_descs)]
       
        return article



