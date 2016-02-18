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

class JFRBSpider(EpaperSpider):

    name = 'JFRB-SH'

    zh_name = u'解放日报'

    publish_date = datetime.today() 
    
    base_url = 'http://newspaper.jfdaily.com/jfrb/html/%s' % publish_date.strftime('%Y-%m/%d')

    start_urls = ['%s/node_2.htm' % base_url,]

    rules = (
        Rule(
            LinkExtractor(allow=('%s/node_\d+\.htm' % base_url),
            deny = ('%s/node_1\.htm' % base_url) ),
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
        page['image'] = {'origin':urljoin(response.url, x.xpath('//img[@id="Img_a"]/@src').extract()[0])}
        page['number'],page['name'] = ''.join(x.xpath('//div[@class="right_4"]/text()').extract()).strip().split(u'：')
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        self._set_coords(response, x)
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        n = ArticleItem()
        n['leadtitle'] = u''.join(x.xpath('//div[@class="title"]/h3[1]/text()').extract()).strip()
        n['title'] = u''.join(x.xpath('//h1/text()').extract()).strip()
        n['subtitle'] = u''.join(x.xpath('//div[@class="title"]/h3[2]/text()').extract()).strip()
        n['url'] = response.url
        n['referer'] = response.request.headers.get('Referer',None)
        n['content'] = u'\n'.join(x.xpath('//div[@class="content"]//text()').extract())
        n['coords'] = self.coords[response.url]
        image_links = [urljoin(response.url,i.replace('\\','/')) for i in (x.xpath('//center//table//tr[2]/td[2]/img/@src').extract())]
        image_descs = x.xpath('//center[last()]//div/text()').extract()
        n['images'] = [{'origin':im[0],'desc':im[1]} for im in zip(image_links,image_descs)]
        return n


