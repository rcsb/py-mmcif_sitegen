##
# File: testDictionaryItemCoverage.py
# Author:  J. Westbrook
# Date:    28-Dec-2020
# Version: 0.001
#
# Update:
##
"""
Tests for dictionary item coverage methods.
"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import time
import unittest

from mmcif.sitegen.dictionary.DictionaryItemCoverage import DictionaryItemCoverage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class DictionaryItemCoverageTests(unittest.TestCase):
    def setUp(self):
        #
        self.__testData = os.path.join(HERE, "test-data")
        self.__coveragePath = os.path.join(self.__testData, "coverage")
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testItemCoverage(self):
        """Test get item counts"""
        try:
            itcov = DictionaryItemCoverage(self.__coveragePath)
            itD = itcov.getItemCoverage(deliveryType="cc")
            self.assertGreater(len(itD), 200)
            itD = itcov.getItemCoverage(deliveryType="bird")
            self.assertGreater(len(itD), 75)
            itD = itcov.getItemCoverage(deliveryType="family")
            self.assertGreater(len(itD), 50)
            itD = itcov.getItemCoverage(deliveryType="archive")
            self.assertGreater(len(itD), 2100)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def dictItemCoverageSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryItemCoverageTests("testItemCoverage"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = dictItemCoverageSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
