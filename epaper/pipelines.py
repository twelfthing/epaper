# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
from datetime import datetime

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from lxml import etree

import settings
from items import PaperItem,PageItem,ArticleItem


class SavePipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def process_item(self, item, spider):
        if not hasattr(spider, 'paper'):
            setattr(spider,'paper',{'pages':[],'articles':{}})
        if isinstance(item,PaperItem):
            spider.paper.update(dict(item))
        elif isinstance(item,PageItem):
            spider.paper['pages'].append(dict(item))
        elif isinstance(item,ArticleItem):
            if not spider.paper['articles'].get(item['referer']):
                spider.paper['articles'][item['referer']] = []
            spider.paper['articles'][item['referer']].append(dict(item))
        return item

    def __get_xml_element(self, spider):
        
        paper = etree.Element('Paper', PaperName=spider.paper['zh_name'], PublishDate=spider.paper['publish_date'], PaperUrl=spider.paper['url'],PaperImageSrc=spider.paper['image']['origin'])
        page_list = etree.SubElement(paper, 'PageList')
        for page in spider.paper['pages']:
            
            page_name = page.get('name','').replace(u'\r\n','').replace(u'\t','').strip()
            page_ele = etree.SubElement(page_list, 'Page', PageNo=page.get('number',''), PageName=page_name, PageImageSrc=page['image']['origin'], PageUrl=page.get('url',''))
            article_list = etree.SubElement(page_ele, 'ArticleList')
            for article in spider.paper['articles'].get(page['url'],[]):
                article_ele = etree.SubElement(article_list, 'Article')
                etree.SubElement(article_ele, 'IntroTitle').text = article.get('leadtitle','')
                etree.SubElement(article_ele, 'Title').text = article.get('title','')
                etree.SubElement(article_ele, 'SubTitle').text = article.get('subtitle','')
                etree.SubElement(article_ele, 'Author').text = article.get('author','')
                etree.SubElement(article_ele, 'Content').text = article.get('content','')
                etree.SubElement(article_ele, 'ArticleUrl').text = article.get('url','')
                image_list_ele = etree.SubElement(article_ele, 'ImageList')   
                for im in article.get('images'):
                    etree.SubElement(image_list_ele, 'Image',Name=im['origin']).text = im.get('desc','')
                point_list = etree.SubElement(article_ele, 'PointList')
                if article['coords']:
                    point_list.text = article['coords']
                else:
                    point_list.text = '0,0,0,0'     
        return paper
             
         

    
    def spider_closed(self, spider):
        if hasattr(spider, 'paper'):
            if hasattr(settings,'JSON_PATH'):
                base_path = os.path.join(settings.JSON_PATH,spider.publish_date.strftime('%Y-%m-%d'))
                if not os.path.isdir(base_path):
                    os.mkdir(base_path)
                path = os.path.join(settings.JSON_PATH,spider.publish_date.strftime('%Y-%m-%d'),spider.name+'.json')
                with open(path,'w') as file_json:
                    file_json.write(json.dumps(spider.paper))
            if hasattr(settings,'IMAGES_PATH'):
                base_path = os.path.join(settings.XML_PATH,spider.publish_date.strftime('%Y-%m-%d'))
                if not os.path.isdir(base_path):
                    os.mkdir(base_path)
                path = os.path.join(settings.XML_PATH,spider.publish_date.strftime('%Y-%m-%d'),spider.name+'.xml')
                with open(path,'w') as file_xml:
                    paper = self.__get_xml_element(spider)
                    xml_str = etree.tostring(paper, encoding='utf-8', xml_declaration=True, pretty_print=True)   
                    file_xml.write(xml_str)         
            setattr(spider, 'paper', None)

