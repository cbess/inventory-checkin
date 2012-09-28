# inventory checkin settings
import os

# `%(app_dir)s` resolves to the directory where iMate is installed.

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False for production or in untrusted environments use)
DEBUG = True

# Should not be changed, this is the absolute path to the directory
# containing main.py, core/, etc.
# type: string
# default: os.path.abspath('.')
ROOT_DIR = os.path.abspath('.')

# An absolute path to the directory path that will store the logs.
# Set to an empty string to disable logging.
# type: string
# default: ''
LOG_PATH = ''

# The name of the server type to use as the web server.
# CherryPy support is built-in, if production: 'cherrypy'.
# type: string
# default: None
SERVER_TYPE = None

# The local port to expose the web server.
# type: integer
# default: 7777
SERVER_PORT = 7777

# The local address to access the web server (the host name to listen on).
# Use '0.0.0.0' to make it available externally.
# type: string
# default: '127.0.0.1' or 'localhost'
SERVER_ADDRESS = '127.0.0.1'

# The banner text displayed in the header of each page.
# type: string/html
# default: 'Sherlock Search'
SITE_BANNER_TEXT = 'Inventory Mate'

# The site title text (displayed in browser tab or title bar of window).
# This is appended to each auto-generated page title.
# type: string
# default: 'iMate'
SITE_TITLE = 'iMate'

# The site banner background color. This banner is shown at the top of each page.
# Possible values: black, blue, skyblue, silver, orange, white
# More colors can be added to 'bg-gradients.css'
# The banner text styles must be changed in the stylesheet: main.css (#top-banner #banner-text)
# type: string
# default: black
SITE_BANNER_COLOR = 'black'


# Customzie the settings per installation
try:
    # Try to import local settings, which override the above settings.
    # In local_settings.py (in this directory), set the values for any settings
    # you want to override.
    from local_settings import *
except ImportError:
    print 'No local_settings.py found. Using all default settings.'
    pass
