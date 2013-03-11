# encoding: utf-8

# try ipython first, fallback to standard pdb
try:
    from ipdb import set_trace
    debug = set_trace
except ImportError:
    from pdb import set_trace
    debug = set_trace
    pass

import codecs
import settings
from datetime import datetime


def read_file(path, encoding='utf-8'):
    """Reads the file at the target path.
    """
    with codecs.open(path, "r", encoding=encoding) as f:
        try:
            contents = f.read()
        except UnicodeDecodeError, e:
            # re-raise with more information
            raise Exception('%s: %s' % (e, path))
    return contents


def safe_read_file(path, ignore_errors=False, encoding='utf-8'):
    """Returns the contents of the file at the specified path. Ignores any
    errors that may occur
    """
    try:
        contents = read_file(path, encoding=encoding)
    except Exception, e:
        if not ignore_errors:
            raise e
        return None
    return contents


def resolve_path(path):
    """Returns the resolved path based on app path variables.
    """
    return path % { 'app_dir' : settings.ROOT_DIR }
    
    
def datetime_to_phrase(date_time):
    """
    converts a python datetime object to the 
    format "X days, Y hours ago"
    
    @param date_time: Python datetime object

    @return:
        fancy datetime:: string
        
    @author: 
        Copyright 2009 Jai Vikram Singh Verma (jaivikram[dot]verma[at]gmail[dot]com)
        http://code.activestate.com/recipes/576880-convert-datetime-in-python-to-user-friendly-repres/
    """
    current_datetime = datetime.now()
    delta = str(current_datetime - date_time)
    if delta.find(',') > 0:
        days, hours = delta.split(',')
        days = int(days.split()[0].strip())
        hours, minutes = hours.split(':')[0:2]
    else:
        hours, minutes = delta.split(':')[0:2]
        days = 0
    days, hours, minutes = int(days), int(hours), int(minutes)
    datelets =[]
    years, months, xdays = None, None, None
    plural = lambda x: 's' if x != 1 else ''
    if days >= 365:
        years = int(days / 365)
        datelets.append('%d year%s' % (years, plural(years)))
        days = days % 365
    if days >= 30 and days < 365:
        months = int(days / 30)
        datelets.append('%d month%s' % (months, plural(months)))        
        days = days % 30
    if not years and days > 0 and days < 30:
        xdays = days
        datelets.append('%d day%s' % (xdays, plural(xdays)))        
    if not (months or years) and hours != 0:
        datelets.append('%d hour%s' % (hours, plural(hours)))        
    if not (xdays or months or years):
        datelets.append('%d minute%s' % (minutes, plural(minutes)))        
    return ', '.join(datelets) + ' ago.'