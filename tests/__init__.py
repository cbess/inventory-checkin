# tests/__init__.py
# setup test env
import logging
import os
import settings
import sys


# setup logger
imate_logger = logging.getLogger('core.imate')
imate_logger.setLevel(logging.DEBUG)
filename = 'imate.tests.log.txt'
hdlr = None
if settings.LOG_PATH:
    hdlr = logging.FileHandler(os.path.join(settings.LOG_PATH, filename, __name__))
else:
    hdlr = logging.StreamHandler(sys.__stdout__)
if hdlr:
    imate_logger.addHandler(hdlr)


def run_all():
    """Runs all unit tests
    """
    # test_checkin.run()
    pass