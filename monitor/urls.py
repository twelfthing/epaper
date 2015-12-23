from handlers.index import IndexHandler
from handlers.websocket import WSHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/ws", WSHandler),
]