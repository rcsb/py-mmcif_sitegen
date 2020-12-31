##
# File: testDictionaryRegistry.py
# Author:  J. Westbrook
# Date:    28-Dec-2020
# Version: 0.001
#
# Update:
##
"""
Tests for dictionary registry access methods.
"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import time
import unittest

from mmcif.sitegen.dictionary.DictionaryRegistry import DictionaryRegistry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class DictionaryRegistryTests(unittest.TestCase):
    def setUp(self):
        #
        self.__testData = os.path.join(HERE, "test-data")
        self.__registryPath = os.path.join(self.__testData, "config", "mmcif_dictionary_registry.json")
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testRegistry(self):
        """Test fetch API"""
        try:
            dr = DictionaryRegistry(self.__registryPath)
            nL = dr.getDictionaryNameList()
            self.assertGreater(len(nL), 10)
            logger.debug("nameList length %d", len(nL))
            nL = dr.getInternalDictionaryNameList()
            self.assertGreater(len(nL), 4)
            nL = dr.getPdbxDictionaryNameList()
            self.assertGreaterEqual(len(nL), 4)

            rD = dr.get()
            self.assertGreater(len(rD), 10)
            for dictName, _ in rD.items():
                qV = dr.getTitle(dictName)
                self.assertIsNotNone(qV)
                qV = dr.getDescription(dictName)
                self.assertIsNotNone(qV)
                qV = dr.getDevelopers(dictName)
                self.assertIsNotNone(qV)
                qV = dr.getMaintainers(dictName)
                self.assertIsNotNone(qV)
                qV = dr.getSchemaName(dictName)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def dictRegistrySuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryRegistryTests("testRegistry"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = dictRegistrySuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
