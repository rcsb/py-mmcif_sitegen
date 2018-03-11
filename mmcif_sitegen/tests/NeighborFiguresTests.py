##
# File:    NeighborFiguresTests
# Author:  jdw
# Date:    13-Aug-2013
# Version: 0.001
#
# Updates:
#
#   3-Oct-2013 jdw reorganize with registry and coverage classes --
#   8-Oct-2013 jdw adjust cellpadding for attribute name display -
#  23-Nov-2013 jdw adjust path for production site and change purge behavior
##
"""
Tests cases for category neighbor diagram figure generator and related classes.

Schema list -

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import sys
import unittest
import time
import os

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif_sitegen import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from mmcif_sitegen import __version__

from mmcif_sitegen.dictionary.HtmlPathInfo import HtmlPathInfo
from mmcif_sitegen.dictionary.DictionaryFileUtils import DictionaryFileUtils
from mmcif_sitegen.dictionary.NeighborFigures import NeighborFigures
from mmcif_sitegen.dictionary.HtmlGenerator import HtmlGenerator
from mmcif_sitegen.dictionary.DictionaryRegistry import DictionaryRegistry, DictionaryItemCoverage


class NeighborFiguresTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        #
        # site path details --
        pathDot = os.getenv("GRAPHVIZ_DOT_BINARY", default=None)
        self.__pathDot = pathDot if pathDot else '/opt/wwpdb/bin/dot'
        #
        #  This is full path to the web site installation directory -
        #
        topPath = os.getenv("DOCS_ONTOLOGIES_TOP")
        self.__webTopPath = topPath if topPath is not None else '/net/www-rcsb/ontologies-prod/docs-ontologies'
        self.__pdbxDocsPath = os.path.join(self.__webTopPath, 'mmcif')
        self.__pdbmlDocsPath = os.path.join(self.__webTopPath, 'pdbml')

        self.__htmlTopDir = 'dictionaries'
        #
        # Install path for dictionary text files in the web directory -
        #
        self.__pdbxResourcePath = os.path.join(self.__pdbxDocsPath, self.__htmlTopDir, 'ascii')
        #
        self.__dR = DictionaryRegistry(verbose=self.__verbose)
        self.__dictionaryNameList = self.__dR.getDictionaryNameList()
        self.__getDictCounts()
        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def __getDictCounts(self, dictionaryName=None, specialFlag=False):
        self.__dIC = DictionaryItemCoverage(dictionaryName=dictionaryName, verbose=self.__verbose)
        self.__archiveItemNameD = self.__dIC.getItemCoverage(deliveryType='archive', specialFlag=specialFlag)
        self.__ccItemNameD = self.__dIC.getItemCoverage(deliveryType='cc')
        self.__prdItemNameD = self.__dIC.getItemCoverage(deliveryType='prd')
        self.__familyItemNameD = self.__dIC.getItemCoverage(deliveryType='family')

    def testMakeSelectedCategoryFigures(self):
        self.__getDictCounts(dictionaryName='mmcif_pdbx_v40', specialFlag=True)
        self.__testMakeSelectedFigures(dictionaryName='mmcif_pdbx_v40', categoryName='entity',
                                       neighborCategoryList=['entity_src_gen', 'entity_src_nat', 'pdbx_entity_src_syn', 'entity_name_com', 'entity_keywords', 'atom_site'],
                                       graphTitle=" <br/>Selected Relationships for Category <b>entity</b>",
                                       graphSubTitle=" in dictionary mmcif_pdbx_v40", titleFormat='html')

        self.__testMakeSelectedFigures(dictionaryName='mmcif_pdbx_v40', categoryName='atom_site',
                                       neighborCategoryList=['entity', 'entity_poly_seq', 'chem_comp', 'chem_comp_atom', 'struct_asym', 'atom_type'],
                                       graphTitle=" <br/>Selected Relationships for Category <b>atom_site</b>",
                                       graphSubTitle=" in dictionary mmcif_pdbx_v40", titleFormat='html')

        self.__testMakeSelectedFigures(dictionaryName='mmcif_pdbx_v40', categoryName='chem_comp',
                                       neighborCategoryList=['chem_comp_atom', 'chem_comp_bond', 'pdbx_chem_comp_descriptor', 'pdbx_chem_comp_identifier', 'pdbx_chem_comp_audit'],
                                       graphTitle=" <br/>Selected Relationships for Category <b>chem_comp</b>",
                                       graphSubTitle=" in dictionary mmcif_pdbx_v40", titleFormat='html',
                                       filterDelivery=True, deliveryType='cc')

        self.__getDictCounts(dictionaryName='mmcif_pdbx_v5_next',
                             specialFlag=True)
        self.__testMakeSelectedFigures(dictionaryName='mmcif_pdbx_v5_next', categoryName='entity_poly', neighborCategoryList=['entity_poly_seq', 'atom_site', 'chem_comp', 'entity'],
                                       graphTitle=" <br/>Selected Relationships for Category <b>entity_poly</b>",
                                       graphSubTitle=" in dictionary mmcif_pdbx_v40", titleFormat='html',
                                       filterDelivery=True, deliveryType='archive')

    def __testMakeSelectedFigures(self, dictionaryName, categoryName, neighborCategoryList=None, graphTitle=None, graphSubTitle=None, titleFormat='text',
                                  filterDelivery=True, deliveryType='archive'):
        """  Render category-level figures for current dictionary list.
        """

        try:
            dictPath = os.path.join(self.__pdbxResourcePath, dictionaryName + '.dic')
            pI = HtmlPathInfo(dictFilePath=dictPath, htmlDocsPath=self.__pdbxDocsPath,
                              htmlTopDirectoryName=self.__htmlTopDir, verbose=self.__verbose)

            dfu = DictionaryFileUtils(dictFilePath=dictPath, verbose=self.__verbose)
            dApi = dfu.getApi()
            self.__getDictCounts(dictionaryName=dictionaryName)
            self.__makeCategoryNeighborFigureSelected(categoryName, neighborCategoryList=neighborCategoryList, dApi=dApi, pathInfoObj=pI,
                                                      graphTitle=graphTitle, graphSubTitle=graphSubTitle, titleFormat=titleFormat, imageFilePath='.',
                                                      filterDelivery=filterDelivery, deliveryType=deliveryType)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testMakeCategoryFiguresAuto(self):
        """  Automated rendering of all category-level figures for current dictionary list.
        """

        try:
            for d in self.__dictionaryNameList:
                logger.debug("\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
                logger.debug("+NeighborFigureTests.testMakeCategoryFiguresAuto() Starting figures generation for dictionary %s\n" % d)
                dictPath = os.path.join(self.__pdbxResourcePath, d + '.dic')
                pI = HtmlPathInfo(dictFilePath=dictPath, htmlDocsPath=self.__pdbxDocsPath,
                                  htmlTopDirectoryName=self.__htmlTopDir, verbose=self.__verbose)

                dfu = DictionaryFileUtils(dictFilePath=dictPath, verbose=self.__verbose)
                dApi = dfu.getApi()
                self.__makeDirectories(pathDictionary=dictPath, pathInfoObj=pI, purge=False)

                categoryNameList = dApi.getCategoryList()
                self.__getDictCounts(dictionaryName=d)
                self.__makeCategoryNeighborFiguresAuto(categoryNameList=categoryNameList, dApi=dApi, pathInfoObj=pI)

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testMakeCategoryFiguresFiltered(self):
        """  Automated rendering of all category-level figures for current dictionary list.
        """

        try:
            for d in self.__dictionaryNameList:
                if d not in ['mmcif_sas', 'mmcif_pdbx_v40', 'mmcif_pdbx_v5_next', 'mmcif_pdbx_v50']:
                    continue
                logger.debug("\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
                logger.debug("+NeighborFigureTests.testMakeCategoryFiguresAuto() Starting figures generation for dictionary %s\n" % d)
                dictPath = os.path.join(self.__pdbxResourcePath, d + '.dic')
                pI = HtmlPathInfo(dictFilePath=dictPath, htmlDocsPath=self.__pdbxDocsPath,
                                  htmlTopDirectoryName=self.__htmlTopDir, verbose=self.__verbose)

                dfu = DictionaryFileUtils(dictFilePath=dictPath, verbose=self.__verbose)
                dApi = dfu.getApi()
                self.__makeDirectories(pathDictionary=dictPath, pathInfoObj=pI, purge=False)

                categoryNameList = dApi.getCategoryList()
                self.__getDictCounts(dictionaryName=d)
                self.__makeCategoryNeighborFiguresAuto(categoryNameList=categoryNameList, dApi=dApi, pathInfoObj=pI)

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def __makeCategoryNeighborFigureSelected(self, categoryName, neighborCategoryList=None, dApi=None, pathInfoObj=None,
                                             graphTitle=None, graphSubTitle=None, titleFormat='text', imageFilePath='.',
                                             filterDelivery=True, deliveryType='archive'):
        """ Create neighbor figures for the input category and neighbor list using the input dictionary api and pathInfo objects.
        """

        try:
            # size=".7,.7"
            size = None
            #
            nf = NeighborFigures(dictApiObj=dApi, pathInfoObj=pathInfoObj, pathDot=self.__pathDot, verbose=self.__verbose)
            nf.setItemCounts(self.__archiveItemNameD, deliveryType='archive')
            nf.setItemCounts(self.__ccItemNameD, deliveryType='cc')
            nf.setItemCounts(self.__prdItemNameD, deliveryType='prd')
            nf.setItemCounts(self.__familyItemNameD, deliveryType='family')
            #

            figureCount = 0
            if graphTitle is None:
                graphTitle = "Category Relationship Diagram for %s " % categoryName
            ok = nf.makeNeighborFigure(categoryName, graphTitle=graphTitle, graphSubTitle=graphSubTitle, titleFormat=titleFormat, format='svg',
                                       size=size, maxItems=50, filterDelivery=filterDelivery, deliveryType=deliveryType,
                                       neighborCategoryList=neighborCategoryList, imageFilePath=imageFilePath)
            if ok:
                figureCount += 1

            logger.debug("+__makeCategoryNeighborFigureSelected() category %s figure count %d\n" % (categoryName, figureCount))
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def __makeCategoryNeighborFiguresAuto(self, categoryNameList, dApi=None, pathInfoObj=None):
        """ Create neighbor figures for input categories using the input dictionary api and pathInfo objects.
        """
        try:
            # size=".7,.7"
            size = None
            #
            nf = NeighborFigures(dictApiObj=dApi, pathInfoObj=pathInfoObj, pathDot=self.__pathDot, verbose=self.__verbose)
            nf.setItemCounts(self.__archiveItemNameD, deliveryType='archive')
            nf.setItemCounts(self.__ccItemNameD, deliveryType='cc')
            nf.setItemCounts(self.__prdItemNameD, deliveryType='prd')
            nf.setItemCounts(self.__familyItemNameD, deliveryType='family')
            #
            dictTitle = dApi.getDictionaryTitle()
            dictVersion = dApi.getDictionaryVersion()

            figureCount = 0
            for categoryName in categoryNameList:

                title = " <br/> <br/> Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                subTitle = " in dictionary %s version %s " % (dictTitle, dictVersion)
                ok = nf.makeNeighborFigure(categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat='html', format='svg', size=size, maxItems=20, filterDelivery=False,
                                           deliveryType='archive')
                if ok:
                    figureCount += 1
                #

                title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                subTitle = " in dictionary %s version %s <br/> including only data categories used in current PDB entries." % (dictTitle, dictVersion)
                ok = nf.makeNeighborFigure(categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat='html', format='svg', size=size, maxItems=20, filterDelivery=True,
                                           deliveryType='archive')

                if ok:
                    figureCount += 1

                if nf.getCategoryUseCount(categoryName, deliveryType='cc') > 0:
                    title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                    subTitle = " in dictionary %s version %s <br/> including only data categories used in the chemical reference dictionary." % (dictTitle, dictVersion)
                    ok = nf.makeNeighborFigure(categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat='html', format='svg', size=size, maxItems=20, filterDelivery=True,
                                               deliveryType='cc')
                    if ok:
                        figureCount += 1

                if (nf.getCategoryUseCount(categoryName, deliveryType='prd') > 0):
                    title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                    subTitle = " in dictionary %s version %s <br/> including only data categories used in the BIRD reference dictionary." % (dictTitle, dictVersion)
                    ok = nf.makeNeighborFigure(categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat='html', format='svg', size=size, maxItems=20, filterDelivery=True,
                                               deliveryType='prd')
                    if ok:
                        figureCount += 1

                if (nf.getCategoryUseCount(categoryName, deliveryType='family') > 0):
                    title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                    subTitle = " in dictionary %s version %s <br/> including only data categories used in the BIRD family reference dictionary." % (dictTitle, dictVersion)
                    ok = nf.makeNeighborFigure(categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat='html', format='svg', size=size, maxItems=20, filterDelivery=True,
                                               deliveryType='family')
                    if ok:
                        figureCount += 1

            logger.debug("+__makeNeighborFigures() %s category count %d figure count %d\n" % (dictTitle, len(categoryNameList), figureCount))
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def __makeDirectories(self, pathDictionary, pathInfoObj=None, purge=True):
        """ Create file system structure for HTML dictionary rendering
        """

        try:
            hg = HtmlGenerator(pathInfoObj=pathInfoObj, verbose=self.__verbose)
            hg.makeDirectories(purge=purge)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suiteNeighborFiguresAutoTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(NeighborFiguresTests("testMakeCategoryFiguresAuto"))
    return suiteSelect


def suiteNeighborFiguresFilteredTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(NeighborFiguresTests("testMakeCategoryFiguresFiltered"))
    return suiteSelect


def suiteNeighborFiguresSelectedTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(NeighborFiguresTests("testMakeSelectedCategoryFigures"))
    return suiteSelect

if __name__ == '__main__':
    if (False):
        mySuite = suiteNeighborFiguresAutoTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    if (False):
        mySuite = suiteNeighborFiguresSelectedTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    # production options
    if (True):
        mySuite = suiteNeighborFiguresFilteredTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
