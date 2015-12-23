#coding=utf-8

"""
    Author: ChengCheng
    Date  : 2015-12-20
"""

import json
from handlers import BaseHandler



class IndexHandler(BaseHandler):

    def get(self):
        self.render('websocket.html')

