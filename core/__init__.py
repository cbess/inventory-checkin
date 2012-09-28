from cherrypy import wsgiserver as cherrypy_wsgiserver
import peewee
import flask
import settings

app = flask.Flask('webapp')
app.config.from_object('webapp.settings')

def get_version_info(module):
    """Returns the version information for the target core module
    :return: string
    """
    module = module.lower()
    if module == 'cherrypy':
        import cherrypy
        return cherrypy.__version__
    elif module == 'flask':
        return flask.__version__
    return '0.0'