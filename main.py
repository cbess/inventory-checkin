#!/usr/bin/env python
# encoding: utf-8
""" 
main.py
Created by Christopher Bess (https://github.com/cbess/inventory-checkin)
Copyright 2012
"""
script_description = 'Runs the main application.'
try:
    # optparse is deprecated, but I wanted broader compatibility
    from optparse import OptionParser
    parser = OptionParser(description=script_description)
    add_argument = parser.add_option
except ImportError:
    # this is here to help any future upgrades
    from argparse import ArgumentParser
    parser = ArgumentParser(description=script_description)
    add_argument = parser.add_argument
    pass

from webapp import server
from core import get_version_info
import tests
import settings
import os
import sys
from datetime import datetime


def get_app_args():
    """Returns the application arguments from stdin
    @return Object optparse.Values or argparse.Namespace
    """
    arguments = parser.parse_args()
    if isinstance(arguments, tuple):
        # assume its optparse return value
        (opts, args) = arguments
        return opts
    return arguments
    

def get_options():
    """ Returns the options from the script """
    add_argument("--test", dest="run_tests",
                    action='store_true',
                      help="Run tests to ensure everything works correctly.")
    add_argument('--runserver', dest='run_server',
                 action='store_true',
                    help='Run the iMate web server.')
    add_argument('-v', '--version', dest='show_version',
                 action='store_true',
                    help='Show iMate version information.')
    # not available, yet
#    add_argument("-q", "--quiet",
#                      action="store_false", dest="verbose", default=True,
#                      help="Don't print status messages to stdout.")
    options = get_app_args()
    return options
    
    
def run():
    options = get_options()
    # determine app action
    if options.run_tests:
        tests.run_all()
    elif options.show_version:
        pyver = sys.version_info
        print '  Python: v%d.%d.%d' % (pyver.major, pyver.minor, pyver.micro)
        print '   Flask: v' + get_version_info('flask')
        print 'CherryPy: v' + get_version_info('cherrypy')
    elif options.run_server:
        print 'Server: %s' % settings.SERVER_TYPE
        # launch web server
        server.run()
    else:
        print 'Use -h to see options.'
    pass
    

if __name__ == '__main__':
    print 'iMate v%s started' % get_version_info('ici')
    run()
    print 'iMate done.'