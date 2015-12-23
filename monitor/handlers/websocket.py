#coding=utf-8

"""
    Author: ChengCheng
    Date  : 2015-12-20
"""
import json
import tornado
import tornadoredis
from tornado.websocket import WebSocketHandler


clients = set()

toredis = tornadoredis.Client()
toredis.connect()

class WSHandler(WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(WSHandler, self).__init__(*args, **kwargs)
        clients.add(self)
        self.listen()

    def on_message(self, message):
        if message.kind == 'message':
            return
        for client in clients:
            client.write_message(message.body)
    @tornado.gen.coroutine
    def listen(self):
        toredis.subscribe('spider.stats')
        toredis.listen(self.on_message)

