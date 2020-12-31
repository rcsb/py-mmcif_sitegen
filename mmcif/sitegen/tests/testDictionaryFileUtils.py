##
# File: testDictionaryFileUtils.py
# Author:  J. Westbrook
# Date:    28-Dec-2020
# Version: 0.001
#
# Update:
##
"""
Tests for dictionary file and api delivery utils.
"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import time
import unittest

from mmcif.sitegen.dictionary.DictionaryFileUtils import DictionaryFileUtils

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class DictionaryFileUtilsTests(unittest.TestCase):
    def setUp(self):
        #
        self.__testData = os.path.join(HERE, "test-data")
        self.__pdbxDictPath = os.path.join(self.__testData, "dictionaries", "mmcif_pdbx_v5_next.dic")
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGetApi(self):
        """Test fetch API"""
        try:
            dfu = DictionaryFileUtils(self.__pdbxDictPath)
            dApi = dfu.getApi()
            version = dApi.getDictionaryVersion()
            logger.debug("version is %r", version)
            self.assertGreater(float(version), 5.0)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def dictApiSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryFileUtilsTests("testGetApi"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = dictApiSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
