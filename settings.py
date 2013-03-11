# inventory checkin settings
import os

# `%(app_dir)s` resolves to the directory where iMate is installed.

# Should not be changed, this is the absolute path to the directory
# containing main.py, core/, etc.
# type: string
# default: os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(__file__)

# A value indicating whether the app runs in debug mode.
# type: boolean
# default: True (set to False if deployed in production or untrusted environments)
DEBUG = True

# An absolute path to the directory path that will store the logs.
# Set to an empty string to disable logging.
# type: string
# default: ''
LOG_PATH = ''

# The name of the server type to use as the web server.
# CherryPy, gevent, and Tornado support is built-in, 
# if production: 'cherrypy' or 'tornado' or 'gevent'.
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
# default: 'InventoryMate'
SITE_BANNER_TEXT = 'InventoryMate'

# The site title text (displayed in browser tab or title bar of window).
# This is appended to each auto-generated page title.
# type: string
# default: 'InventoryMate'
SITE_TITLE = 'InventoryMate'

# The site banner background color. This banner is shown at the top of each page.
# Possible values: black, blue, skyblue, silver, orange, white
# More colors can be added to 'bg-gradients.css'
# The banner text styles must be changed in the stylesheet: main.css (#top-banner #banner-text .brand)
# type: string
# default: None (soft white)
SITE_BANNER_COLOR = None

# The mongo database connection settings.
# Supports:
#   DB = database name (required)
#   HOST = hostname (optional, default: localhost)
#   PORT = port (optional, default: 27017)
#   USERNAME = username (optional)
#   PASSWORD = password (optional)
#
# type: string
# default: inventorymate
DATABASE = {
    'DB' : 'inventorymate',
}

# The name of the inventory items
# type: string
# default: Inventory
INVENTORY_ITEM_NAME = 'Inventory'
INVENTORY_ITEM_NAME_PLURAL = 'Inventory'

# Regular expression that grabs a group which contains the
# number that is used for sorting the items.
# This is useful if the item names have numbers
# default: None (post DB sorting, sorts by name ascending)
INVENTORY_ITEM_NAME_SORT_NUMBER_REGEX = None

# A value indicating rather the user must confirm an action.
# default: { 'checkin' : False }
USER_CONFIRMATION = {
    'checkin' : False
}

# The number of seconds to elapse before the inventory list auto-refreshes. This 
# is for readonly inventory users. Set to zero to disable auto-refresh.
# default: 30 (secs)
INVENTORY_AUTO_REFRESH = 30

# Checkout date format
# ref: http://docs.python.org/2/library/time.html#time.strftime
# default: '%m/%d/%Y %I:%M%p'
INVENTORY_CHECKOUT_DATE_FORMAT = '%m/%d/%Y %I:%M%p'


# Customzie the settings per installation
try:
    # Try to import local settings, which override the above settings.
    # In local_settings.py (in this directory), set the values for any settings
    # you want to override.
    from local_settings import *
except ImportError:
    print 'No local_settings.py found. Using all default settings.'
