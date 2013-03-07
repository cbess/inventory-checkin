from cherrypy import wsgiserver as cherrypy_wsgiserver
import peewee
from flask.ext.mongoengine import MongoEngine
import flask
import settings

app = flask.Flask('webapp')
app.config.from_object('webapp.settings')

db = MongoEngine()
db.init_app(app)


def get_version_info(module):
    """Returns the version information for the target core module
    :return: string
    """
    module = module.lower()
    if module == 'cherrypy':
        import cherrypy
        return cherrypy.__version__
    elif module == 'mongoengine':
        import mongoengine
        return mongoengine.__version__
    elif module == 'flask':
        return flask.__version__
    return '0.0'


LONG_DATE_FORMAT = '%A, %B %d, %Y %I:%M %p'
DEFAULT_DATE_FORMAT = '%m/%d/%Y %I:%M %p'
SHORT_DATE_FORMAT = '%m/%d/%Y %H:%M'
