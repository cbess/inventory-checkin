# Tornado server add-on
# pip install tornado
# ref:
# http://www.tornadoweb.org/documentation/index.html

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app
from core import settings as core_settings


def run():
    """Run the Tornado server"""
    http_server = HTTPServer(WSGIContainer(app))
    http_server.bind(core_settings.SERVER_PORT)
    try:
        http_server.start(0)  # Forks multiple sub-processes
        IOLoop.instance().start()
    except KeyboardInterrupt:
        http_server.stop()
        IOLoop.instance().stop()
