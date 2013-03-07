# http://werkzeug.pocoo.org/docs/serving/#werkzeug.serving.run_simple
from core import settings as core_settings
from core import app
import webapp.settings

def get_server_type():
    stype = core_settings.SERVER_TYPE
    if not stype or stype == 'default':
        return 'werkzeug (default)'
    return stype

# may need to comment out to run adhoc scripts (ex: migration)
import views

def run():
    """Runs the flask server
    """
    # pre server start
    from webapp import admin
    from webapp import models
    admin.setup()
    models.setup()
    
    # start/run server
    server_type = core_settings.SERVER_TYPE
    if server_type == 'cherrypy':
        # near-production level server (small to medium traffic)
        import server_cherrypy
        server_cherrypy.run()
    elif server_type == 'tornado':
        import server_tornado
        server_tornado.run()
    elif server_type == 'gevent':
        import server_gevent
        server_gevent.run()
    else: # default server (flask/werkzeug)
        # dev or low traffic
        app.run(
            host=core_settings.SERVER_ADDRESS,
            port=core_settings.SERVER_PORT,
            debug=core_settings.DEBUG,
            # True if the web server process should handle each request in a separate thread.
            # You can only have one or the other; multi-threaded or multi-process.
            threaded=True,
            # The number of processes to spawn for the server.
            # You can only have one or the other; multi-threaded or multi-process.
            processes=1
        )
