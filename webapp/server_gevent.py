# gevent server add-on
#
# Install:
# brew install libevent
# pip install gevent greenlet
#
# ref:
# http://www.gevent.org/contents.html

from gevent.wsgi import WSGIServer
from server import app
from core import settings as core_settings


def run():
    """Run gevent server"""
    http_server = WSGIServer((core_settings.SERVER_ADDRESS, core_settings.SERVER_PORT), app)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.stop()