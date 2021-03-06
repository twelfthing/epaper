# coding=utf-8

"""
    Author: ChengCheng
    Date  : 2015-12-20
"""
import os
import tornado.web
import tornado.ioloop
import tornado.httpserver

from . import setup
from urls import url_patterns

setup()

def main():
    app = tornado.web.Application(
        url_patterns,
        autoreload=True,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    server = tornado.httpserver.HTTPServer(app)
    server.listen(9100)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
