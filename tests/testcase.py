#!/usr/bin/env python
# encoding: utf-8
"""
testcase.py

Copyright (c) 2012 Christopher Bess. All rights reserved.
"""

import unittest
import sys
import os
import time
import settings


def run_all(testCase):
    """Runs all the tests for the specified test case
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(testCase)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    pass
    
    
class BaseTestCase(unittest.TestCase):
    """ The base class for all test cases """
    
    def setUp(self):
        pass

    def get_test_string(self):
        """
        Gets a string time tuple
        
        Used to ensure the text generated is 'unique'
        
        @return: a string of the current time
        """
        return "current time tuple: %s" % time.localtime()
