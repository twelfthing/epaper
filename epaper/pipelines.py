# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SaveJSONPipeline(object):
    def process_item(self, item, spider):
        if not hasattr(spider, 'items'):
            setattr(spider,'items',{'paper':None,'pages':[])
        if isinstance(item,PaperItem):
            spider.items['paper'] = item
        elif isinstance(item,PageItem):
            spider.items['pages'].append(item)
        elif isinstance(item,ArticleItem):
            if not spider.items['articles'].get(item['referer']):
                spider.items['articles'][item['referer']] = []
            spider.items['articles'][item['referer']].append(item)
        return item
    
    def spider_closed(self, spider):
        if hasattr(spider, 'items'):

            setattr(spider, 'items', None)