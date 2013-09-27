import os
import sys
import unittest


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from test_urllib2 import *
from test_urlfetch import *
from test_pycurl import *
from test_pm import *


if 'CI_SERVER' in os.environ:
    from xmlrunner import XMLTestRunner
    runner = XMLTestRunner
else:
    from unittest import TextTestRunner
    runner = TextTestRunner


if __name__ == '__main__':
    unittest.main(testRunner=runner, verbosity=2)
