# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class EpaperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PaperItem(Item):
    '''Paper item object
    Attributes: 
        name : 报纸名称
        url  : 原始url
        image: 首版图
        publish_date: 发布时间
        fetch_date  : 抓取时间
    '''
    name = Field()
    url = Field()
    image = Field()
    publish_date = Field()
    fetch_date = Field()

    
class PageItem(Item):
    '''版面
    Attributes:
        number :版次
        name   :版名
    '''
    number = Field()
    name = Field()
    url = Field()
    image = Field()
    fetch_date = Field()
    referer = Field()

    
class ArticleItem(Item):
    '''文章
    Attributes:
        images: {origin:'',url:'',desc:''}
        coords: 坐标
        content:内容，带html标签
    '''
    title = Field()
    subtitle = Field()
    leadtitle = Field()
    author = Field()
    images = Field()
    coords = Field()
    content = Field()
    url = Field()
    fetch_date = Field()
    referer = Field()

