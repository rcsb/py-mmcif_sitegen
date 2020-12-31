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
Tests cases for selected category neighbor diagram figure generator.
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import logging
import os
import time
import unittest

from mmcif.sitegen.dictionary import __version__
from mmcif.sitegen.dictionary.DictionaryFileUtils import DictionaryFileUtils
from mmcif.sitegen.dictionary.DictionaryItemCoverage import DictionaryItemCoverage
from mmcif.sitegen.dictionary.DictionaryRegistry import DictionaryRegistry
from mmcif.sitegen.dictionary.HtmlPathInfo import HtmlPathInfo
from mmcif.sitegen.dictionary.NeighborFigures import NeighborFigures

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))


class NeighborFiguresTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True
        self.__fullTest = False
        #
        # site path details --
        self.__pathDot = self.__findGraphvizDot()
        #
        #  This is full path to the web site installation directory -
        #
        self.__workPath = os.path.join(HERE, "test-output")
        self.__testData = os.path.join(HERE, "test-data")
        self.__webTopPath = os.path.join(self.__workPath, "site")
        self.__pdbxDocsPath = os.path.join(self.__webTopPath, "mmcif")
        self.__pdbmlDocsPath = os.path.join(self.__webTopPath, "pdbml")
        self.__htmlTopDir = "dictionaries"
        #
        # Install path for dictionary text files in the web directory -
        #
        self.__pdbxResourcePath = os.path.join(self.__testData, "dictionaries")
        self.__coveragePath = os.path.join(self.__testData, "coverage")
        self.__registryPath = os.path.join(self.__testData, "config", "mmcif_dictionary_registry.json")
        self.__dR = DictionaryRegistry(self.__registryPath)
        if self.__fullTest:
            self.__dictionaryNameList = self.__dR.getDictionaryNameList()
        else:
            self.__dictionaryNameList = ["mmcif_pdbx_v5_next"]
        self.__deliveryTypeL = ["archive", "cc", "prd", "family"]
        self.__itemCountD = self.__getItemCounts(self.__deliveryTypeL)
        self.__startTime = time.time()
        logger.info("Running tests on version %s", __version__)
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def __findGraphvizDot(self):
        pathDot = os.getenv("GRAPHVIZ_DOT_BINARY", default=None)
        pthList = [pathDot] if pathDot else []
        pthList.extend(["/usr/bin/dot", "/usr/local/bin/dot", "/opt/bin/dot"])
        for pth in pthList:
            if os.path.isfile(pth) and os.access(pth, os.X_OK):
                return pth
        return None

    def __getItemCounts(self, deliveryTypeL):
        itemCountD = {}
        self.__dIC = DictionaryItemCoverage(self.__coveragePath)
        for deliveryType in deliveryTypeL:
            itemCountD[deliveryType] = self.__dIC.getItemCoverage(deliveryType=deliveryType)
        for dT, cD in itemCountD.items():
            logger.debug("dT %r length %d", dT, len(cD))
        return itemCountD

    #
    def testMakeSelectedCategoryFigures(self):
        self.__testMakeSelectedFigures(
            dictionaryName="mmcif_pdbx_v5_next",
            categoryName="entity",
            neighborCategoryList=["entity_src_gen", "entity_src_nat", "pdbx_entity_src_syn", "entity_name_com", "entity_keywords", "atom_site"],
            graphTitle=" <br/>Selected Relationships for Category <b>entity</b>",
            graphSubTitle=" in dictionary mmcif_pdbx_v5_next",
            titleFormat="html",
            filterDelivery=True,
            deliveryType="archive",
        )

        self.__testMakeSelectedFigures(
            dictionaryName="mmcif_pdbx_v5_next",
            categoryName="atom_site",
            neighborCategoryList=["entity", "entity_poly_seq", "chem_comp", "chem_comp_atom", "struct_asym", "atom_type"],
            graphTitle=" <br/>Selected Relationships for Category <b>atom_site</b>",
            graphSubTitle=" in dictionary mmcif_pdbx_v5_next",
            titleFormat="html",
            filterDelivery=True,
            deliveryType="archive",
        )

        self.__testMakeSelectedFigures(
            dictionaryName="mmcif_pdbx_v5_next",
            categoryName="chem_comp",
            neighborCategoryList=["chem_comp_atom", "chem_comp_bond", "pdbx_chem_comp_descriptor", "pdbx_chem_comp_identifier", "pdbx_chem_comp_audit"],
            graphTitle=" <br/>Selected Relationships for Category <b>chem_comp</b>",
            graphSubTitle=" in dictionary mmcif_pdbx_v5_next",
            titleFormat="html",
            filterDelivery=True,
            deliveryType="cc",
        )

        self.__testMakeSelectedFigures(
            dictionaryName="mmcif_pdbx_v5_next",
            categoryName="entity_poly",
            neighborCategoryList=["entity_poly_seq", "atom_site", "chem_comp", "entity"],
            graphTitle=" <br/>Selected Relationships for Category <b>entity_poly</b>",
            graphSubTitle=" in dictionary mmcif_pdbx_v5_next",
            titleFormat="html",
            filterDelivery=True,
            deliveryType="archive",
        )

    def __testMakeSelectedFigures(
        self, dictionaryName, categoryName, neighborCategoryList=None, graphTitle=None, graphSubTitle=None, titleFormat="text", filterDelivery=True, deliveryType="archive"
    ):
        """Render category-level figures for the input current category list."""

        try:
            dictPath = os.path.join(self.__pdbxResourcePath, dictionaryName + ".dic")
            pI = HtmlPathInfo(dictFilePath=dictPath, htmlDocsPath=self.__pdbxDocsPath, htmlTopDirectoryName=self.__htmlTopDir, verbose=self.__verbose)

            dfu = DictionaryFileUtils(dictFilePath=dictPath, verbose=self.__verbose)
            dApi = dfu.getApi()
            self.__makeCategoryNeighborFigureSelected(
                categoryName,
                neighborCategoryList=neighborCategoryList,
                dApi=dApi,
                pathInfoObj=pI,
                graphTitle=graphTitle,
                graphSubTitle=graphSubTitle,
                titleFormat=titleFormat,
                imageFilePath=os.path.join(HERE, "test-output"),
                filterDelivery=filterDelivery,
                deliveryType=deliveryType,
            )
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def __makeCategoryNeighborFigureSelected(
        self,
        categoryName,
        neighborCategoryList=None,
        dApi=None,
        pathInfoObj=None,
        graphTitle=None,
        graphSubTitle=None,
        titleFormat="text",
        imageFilePath=".",
        filterDelivery=True,
        deliveryType="archive",
    ):
        """Create neighbor figures for the input category and neighbor list using the input dictionary api and pathInfo objects."""

        try:
            # size=".7,.7"
            size = None
            #
            nf = NeighborFigures(dictApiObj=dApi, pathInfoObj=pathInfoObj, pathDot=self.__pathDot, verbose=self.__verbose)
            for dT in self.__deliveryTypeL:
                nf.setItemCounts(self.__itemCountD[deliveryType], deliveryType=dT)
            #
            figureCount = 0
            if graphTitle is None:
                graphTitle = "Category Relationship Diagram for %s " % categoryName
            ok = nf.makeNeighborFigure(
                categoryName,
                graphTitle=graphTitle,
                graphSubTitle=graphSubTitle,
                titleFormat=titleFormat,
                figFormat="svg",
                size=size,
                maxItems=50,
                filterDelivery=filterDelivery,
                deliveryType=deliveryType,
                neighborCategoryList=neighborCategoryList,
                imageFilePath=imageFilePath,
            )
            if ok:
                figureCount += 1

            logger.debug("category %s figure count %d\n", categoryName, figureCount)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteNeighborFiguresSelectedTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(NeighborFiguresTests("testMakeSelectedCategoryFigures"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = suiteNeighborFiguresSelectedTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
