# -*- coding: utf-8 -*-

# Scrapy settings for epaper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
BOT_NAME = 'epaper'

SPIDER_MODULES = ['epaper.spiders']
NEWSPIDER_MODULE = 'epaper.spiders'
ITEM_PIPELINES = [
    'epaper.pipelines.SaveJSONPipeline'
]
#LOG_FILE = '%s/log/%s_ace.log' %(PROJECT_ROOT,datetime.today().strftime('%Y-%m-%d'))
LOG_LEVEL = 'INFO'
IMAGES_PATH = os.path.join(PROJECT_ROOT, 'images')
JSON_PATH = os.path.join(PROJECT_ROOT, 'json')
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'epaper (+http://www.yourdomain.com)'
