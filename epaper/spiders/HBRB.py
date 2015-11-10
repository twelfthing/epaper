# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
from datetime import datetime

from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.linkextractors.regex import RegexLinkExtractor



from epaper.items import PaperItem, PageItem, ArticleItem
from epaper.spiders.base import EpaperSpider

class HBRBSpider(EpaperSpider):

    name = '湖北日报'

    publish_date = datetime.today() 

    base_url = 'http://ctdsb.cnhubei.com/HTML/hbrb/%s' % publish_date.strftime('%Y%m%d')

    start_urls = ['%s/hbrb1.html' % base_url,]
    
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
        reqs = []
        page = PageItem()
        page['image'] = {'origin':urljoin(response.url, x.xpath('//img[@usemap="#FPMap0"]/@src').extract()[0])}
        nn = x.xpath('//td[@height="30"]/span[@class="STYLE1"]/text()').extract()[0]
        if nn and len(nn)>1:
            page['number'] = nn.split(u' ')[0].strip()
            page['name'] = nn.split(u' ')[1].strip()
        page['url'] = response.url
        reqs.append(page);
        for href in x.xpath('//area/@href').extract():
            reqs.append(Request(urljoin(response.url,href),callback=self.parse_article))
        if response.url == self.start_urls[0]:
            for page in x.xpath('//td[@class="info3"]/@onclick').extract()[1:]:
                href = re.search(r"'(.*?)'", page).group(1)
                url = '%s/%s' %(self.base_url,href)
                reqs.append(Request(url, callback=self.parse_page))
        return reqs

    def parse_article(self, response):
        x = Selector(response)
        article = ArticleItem()
        article['leadtitle'] = u''.join(x.xpath('//table[@id="Table17"]//tr[1]/td/text()').extract()).strip()
        article['title'] = u''.join(x.xpath('//td[@height="40"]/text()').extract()).strip()
        article['subtitle'] = u''.join(x.xpath('//td[@height="25"]/text()').extract()[-1]).strip()
        article['url'] = response.url
        article['referer'] = response.request.headers.get('Referer',None)
        article['content'] = u'\n'.join(x.xpath('//div[@id="copytext"]//font//text()').extract())
        areas = x.xpath('//area')
        for a in areas:
            href = a.xpath('@href').extract()[0].strip()
            coords = a.xpath('@coords').extract()[0]
            if article['url'] == urljoin(response.url, href):
                article['coords'] = coords
                break
        article['images'] = [{'origin':im} for im in x.xpath('//div[@id="copytext"]//img/@src').extract()] 
        return article
