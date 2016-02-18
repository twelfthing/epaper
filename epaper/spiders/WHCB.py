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

class  WHCBSpider(EpaperSpider):

    name = 'WHCB-HB'

    zh_name = u'武汉晨报'

    publish_date = datetime.today()

    base_url = 'http://whcb.cjn.cn/html/%s' % publish_date.strftime('%Y-%m/%d')

    start_urls = ['%s/node_42.htm' % base_url,]

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
        page['image'] = {'origin':urljoin(response.url, x.xpath('//img[@usemap="#PagePicMap"]/@src').extract()[0])}
        page['number'],page['name'] = ''.join(x.xpath('//td[@width="145"]//text()').extract()).split(u'：')
        page['url'] = response.url
        reqs.append(page)
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        self._set_coords(response, x)
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
        article['coords'] = self.coords[response.url]
        image_links = x.xpath('//td[@class="font6"]//img//@src').extract()
        image_descs = [''.join(i.xpath('text()').extract()) for i in x.xpath('//td[@class="font6"]//img/../p')]
        article['images'] = [{'origin':urljoin(response.url,im[0]), 'desc':im[1]} for im in zip(image_links,image_descs)]
       

        return article


