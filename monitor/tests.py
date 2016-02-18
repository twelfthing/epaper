from tornado import gen
from tornado.httpclient import AsyncHTTPClient

url = "http://www.baidu.com"
http_client = AsyncHTTPClient()

@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url)
                        for url in urls}
    # responses is a dict {url: HTTPResponse}
print parallel_fetch_dict([url])