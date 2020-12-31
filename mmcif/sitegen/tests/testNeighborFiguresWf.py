##
# File:    NeighborFiguresTests
# Author:  jdw
# Date:    28-Dec-2020
# Version: 0.001
#
# Updates:
#
##
"""
Tests cases for workflow to generate category neighbor diagram figures.
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import logging
import os
import time
import unittest

from mmcif.sitegen.wf.NeighborFiguresWf import NeighborFiguresWf

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))


class NeighborFiguresWfTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True
        self.__workPath = os.path.join(HERE, "test-output")
        self.__testData = os.path.join(HERE, "test-data")
        self.__websiteGenPath = os.path.join(self.__workPath, "site", "mmcif_website_generated")
        self.__websiteFileAssetsPath = os.path.join(self.__testData)
        self.__testModeFlag = True
        #
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testWorkflow(self):
        """Test workflow to render dictionaries in HTML --"""
        try:
            nfWf = NeighborFiguresWf(websiteGenPath=self.__websiteGenPath, websiteFileAssetsPath=self.__websiteFileAssetsPath, testMode=self.__testModeFlag)
            ok = nfWf.run()
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteWorkflowTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(NeighborFiguresWfTests("testWorkflow"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = suiteWorkflowTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
