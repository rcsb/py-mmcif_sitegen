##
# File:    HtmlGeneratorTests.py
# Author:  jdw
# Date:    13-Aug-2013
# Version: 0.001
#
# Updates:
#     2-Oct-2013  jdw implement reusable DictionaryRegisty for shared dictionary details.
#     3-Oct-2013  jdw implement DictionaryItemCoverage item usage details.
#     6-Oct-2013  jdw history lists order options added
#    23-Nov-2013  jdw update to production paths, prune legacy dictionaries and add PDBML support
##
"""
Tests cases for dictionary HTML rendering.

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
import stat

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

from mmcif_sitegen.dictionary.HtmlGenerator import HtmlGenerator, HtmlTemplates
from mmcif_sitegen.dictionary.HtmlPathInfo import HtmlPathInfo
from mmcif_sitegen.dictionary.DictionaryFileUtils import DictionaryFileUtils
from mmcif_sitegen.dictionary.HtmlContentUtils import HtmlContentUtils
from mmcif_sitegen.dictionary.HtmlMarkupUtils import HtmlMarkupUtils, HtmlComponentMarkupUtils
from mmcif_sitegen.dictionary.DictionaryRegistry import DictionaryRegistry, DictionaryItemCoverage


class HtmlGeneratorTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        #
        # site path details --
        #
        topPath = os.getenv("DOCS_ONTOLOGIES_TOP")
        self.__webTopPath = topPath if topPath is not None else '/net/www-rcsb/ontologies-prod/docs-ontologies'
        self.__pdbxDocsPath = os.path.join(self.__webTopPath, 'mmcif')
        self.__pdbmlDocsPath = os.path.join(self.__webTopPath, 'pdbml')
        #
        self.__htmlTopDir = 'dictionaries'
        #
        # install path for dictionary text files in the web directory -
        #
        self.__pdbxResourcePath = os.path.join(self.__pdbxDocsPath, self.__htmlTopDir, 'ascii')
        self.__pdbmlResourcePath = os.path.join(self.__pdbmlDocsPath, 'schema')
        #
        self.__dR = DictionaryRegistry(verbose=self.__verbose)
        self.__dictionaryNameList = self.__dR.getDictionaryNameList()
        self.__internalDictionaryNameList = self.__dR.getInternalDictionaryNameList()
        #
        self.__schemaNameList = self.__dR.getPdbmlSchemaNameList()
        #
        self.__fullDictionaryNameList = []
        self.__fullDictionaryNameList.extend(self.__dictionaryNameList)
        self.__fullDictionaryNameList.extend(self.__internalDictionaryNameList)
        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        self.__startTime = time.time()
        logger.debug("Running tests on version %s" % __version__)
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def testRenderDictionaries(self):
        """  Render dictionaries in HTML --
        """

        try:
            self.__renderDownloadList()
            for d in self.__fullDictionaryNameList:
                logger.debug("\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
                logger.debug("+HtmlGeneratorTests.testRenderDictionaries() Starting dictionary %s\n" % d)
                dictPath = os.path.join(self.__pdbxResourcePath, d + '.dic')
                self.__makeDirectories(pathDictionary=dictPath)
                leadingGroupList = None
                if d == 'mmcif_mdb':
                    leadingGroupList = ['mdb_group']
                elif d == 'mmcif_sas':
                    leadingGroupList = ['sas_group']
                elif d == 'mmcif_nef':
                    leadingGroupList = ['nef_group']
                elif d == 'mmcif_ihm':
                    leadingGroupList = ['ihm_group']

                self.__renderHtmlDictionary(dictionaryName=d, pathDictionary=dictPath, leadingGroupList=leadingGroupList)

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def __makeDirectories(self, pathDictionary):
        """ Create file system structure for HTML dictionary rendering
        """

        try:
            pI = HtmlPathInfo(dictFilePath=pathDictionary,
                              htmlDocsPath=self.__pdbxDocsPath,
                              htmlTopDirectoryName=self.__htmlTopDir,
                              verbose=self.__verbose)

            hg = HtmlGenerator(pathInfoObj=pI, verbose=self.__verbose)
            hg.makeDirectories(purge=False)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def __writeAnyFile(self, title, subTitle, filePath, htmlContentList, flavor="PDBx"):
        """  Render any page using common header and footer.

             Input HTML content list is inserted within the body of the page.

        """
        try:
            if (self.__verbose):
                logger.debug("HtmlGenerator.writeAnyFile() writing file flavor %s path %s\n" % (flavor, filePath))

            ht = HtmlTemplates()
            ofh = open(filePath, 'w')
            pageTitle = str(title) + " " + str(subTitle)
            if flavor in ['PDBx']:
                ofh.write("%s\n" % ht.getPageHeader(title=pageTitle))
            elif flavor in ['PDBML']:
                ofh.write("%s\n" % ht.getPdbmlPageHeader(title=pageTitle))
            else:
                ofh.write("%s\n" % ht.getPageHeader(title=pageTitle))
            ofh.write("%s\n" % ht.getPageTitle(title, subTitle))
            ofh.write("%s" % '\n'.join(htmlContentList))
            ofh.write("%s\n" % ht.getPageTrailer())
            ofh.close()
            st = os.stat(filePath)
            os.chmod(filePath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            return True
        except Exception as e:
            logger.error("HtmlGenerator.writeAnyFile() failed for %s\n" % (filePath))
            logger.exception("Failing with %s" % str(e))
        return False

    #
    def __makePdbxDownloadPage(self, dictionaryNameList, dictionaryInfoD, dictionaryPath='/dictionaries', schemaPath='/schema'):
        """  Make the download list of PDBx dictionaries
        """
        mU = HtmlMarkupUtils(verbose=self.__verbose)
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginDescriptionList(style="vertical")
        for dictionaryName in dictionaryNameList:
            dList = []
            url = os.path.join(dictionaryPath, dictionaryName + '.dic', 'Index')
            dList.append(mU.getAnchor(contentUrl=url, contentLabel='Dictionary Browser  &raquo;', cssClassString=None, format="html"))

            url = os.path.join(dictionaryPath, 'ascii', dictionaryName + '.dic')
            dList.append(mU.getAnchor(contentUrl=url, contentLabel='Dictionary Text  &raquo;', cssClassString=None, format="html"))

            url = os.path.join(dictionaryPath, 'ascii', dictionaryName + '.dic.gz')
            dList.append(mU.getAnchor(contentUrl=url, contentLabel='Dictionary Text (gz)  &raquo;', cssClassString=None, format="html"))

            if dictionaryInfoD[dictionaryName]['schema'] is not None:
                url = os.path.join(schemaPath, dictionaryInfoD[dictionaryName]['schema'] + '.xsd')
                dList.append(mU.getAnchor(contentUrl=url, contentLabel='PDBML Schema  &raquo;', cssClassString=None, format="html"))
            #
            tS = dictionaryInfoD[dictionaryName]['title']
            dS = dictionaryInfoD[dictionaryName]['description'] + '<br />' + '&nbsp;|&nbsp;'.join(dList)
            html.addDescription(termSt=tS, descriptionSt=dS, formatTerm='html', formatDescription='html', extraSpace=True)

        html.endDescriptionList()
        return html.getHtmlList()

    def __makePdbmlDownloadPage(self, dictionaryNameList, dictionaryInfoD, dictionaryPath='/dictionaries', schemaPath='/schema'):
        """  Make the download list of PDBML schema -
        """
        mU = HtmlMarkupUtils(verbose=self.__verbose)
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginDescriptionList(style="vertical")
        for dictionaryName in dictionaryNameList:
            dList = []
            if dictionaryInfoD[dictionaryName]['schema'] is not None:
                url = os.path.join(schemaPath, dictionaryInfoD[dictionaryName]['schema'] + '.xsd')
                dList.append(mU.getAnchor(contentUrl=url, contentLabel='PDBML Schema  &raquo;', cssClassString=None, format="html"))

                if 'dictionary' in dictionaryInfoD[dictionaryName]:
                    myName = dictionaryInfoD[dictionaryName]['dictionary']
                else:
                    myName = dictionaryName

                url = os.path.join(dictionaryPath, myName + '.dic', 'Index')
                dList.append(mU.getAnchor(contentUrl=url, contentLabel='Dictionary Browser  &raquo;', cssClassString=None, format="html"))

                url = os.path.join(dictionaryPath, 'ascii', myName + '.dic')
                dList.append(mU.getAnchor(contentUrl=url, contentLabel='Dictionary Text  &raquo;', cssClassString=None, format="html"))

                url = os.path.join(dictionaryPath, 'ascii', myName + '.dic.gz')
                dList.append(mU.getAnchor(contentUrl=url, contentLabel='Dictionary Text (gz)  &raquo;', cssClassString=None, format="html"))
                #
                tS = 'PDBML schema for the ' + dictionaryInfoD[dictionaryName]['title']
                dS = dictionaryInfoD[dictionaryName]['description'] + '<br />' + '&nbsp;|&nbsp;'.join(dList)
                html.addDescription(termSt=tS, descriptionSt=dS, formatTerm='html', formatDescription='html', extraSpace=True)

        html.endDescriptionList()
        return html.getHtmlList()

    def __renderDownloadList(self):
        """ Create HTML pages for the input dictionary --
        """

        try:
            filePath = os.path.join(self.__pdbxDocsPath, self.__htmlTopDir, 'downloads.html')
            htmlContentList = self.__makePdbxDownloadPage(dictionaryNameList=self.__dictionaryNameList, dictionaryInfoD=self.__dR.get(),
                                                          dictionaryPath='/dictionaries', schemaPath='/schema')
            self.__writeAnyFile(title='Browse/Download ', subTitle='Dictionaries and Schema', filePath=filePath, htmlContentList=htmlContentList)
            #
            filePath = os.path.join(self.__pdbxDocsPath, self.__htmlTopDir, 'internal-downloads.html')
            htmlContentList = self.__makePdbxDownloadPage(dictionaryNameList=self.__internalDictionaryNameList, dictionaryInfoD=self.__dR.get(),
                                                          dictionaryPath='/dictionaries', schemaPath='/schema')
            self.__writeAnyFile(title='Browse/Download ', subTitle='Internal Dictionaries and Schema', filePath=filePath, htmlContentList=htmlContentList)

            #
            filePath = os.path.join(self.__pdbmlResourcePath, 'pdbml-downloads.html')
            htmlContentList = self.__makePdbmlDownloadPage(dictionaryNameList=self.__schemaNameList, dictionaryInfoD=self.__dR.get(),
                                                           dictionaryPath='/dictionaries', schemaPath='/schema')
            self.__writeAnyFile(title='Browse/Download ', subTitle='PDBML Schema', filePath=filePath, htmlContentList=htmlContentList, flavor="PDBML")

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def __renderHtmlDictionary(self, dictionaryName, pathDictionary, leadingGroupList=None):
        """ Create HTML pages for the input dictionary --
        """

        try:
            pI = HtmlPathInfo(dictFilePath=pathDictionary, htmlDocsPath=self.__pdbxDocsPath,
                              htmlTopDirectoryName=self.__htmlTopDir, verbose=self.__verbose)
            hg = HtmlGenerator(pathInfoObj=pI, verbose=self.__verbose)

            dfu = DictionaryFileUtils(dictFilePath=pathDictionary, verbose=self.__verbose)

            dApi = dfu.getApi()
            hcU = HtmlContentUtils(dictApiObj=dApi, pathInfoObj=pI, verbose=self.__verbose)
            #
            #

            dIC = DictionaryItemCoverage(dictionaryName=dictionaryName,
                                         verbose=self.__verbose)
            archiveItemNameD = dIC.getItemCoverage(deliveryType='archive')
            ccItemNameD = dIC.getItemCoverage(deliveryType='cc')
            prdItemNameD = dIC.getItemCoverage(deliveryType='prd')

            hcU.setItemCounts(archiveItemNameD, deliveryType='archive')
            hcU.setItemCounts(ccItemNameD, deliveryType='cc')
            hcU.setItemCounts(prdItemNameD, deliveryType='prd')

            try:
                tS = self.__dR.getTitle(dictionaryName=dictionaryName)
                dS = self.__dR.getDescription(dictionaryName=dictionaryName)
                aS = self.__dR.getDevelopers(dictionaryName=dictionaryName)
                mS = self.__dR.getMaintainers(dictionaryName=dictionaryName)
            except Exception as e:
                logger.warn("\nMissing dictionary info for %s\n" % (dictionaryName))
                tS = None
                dS = None
                aS = None
                mS = None
            downloadPath = os.path.join('/', self.__htmlTopDir, 'ascii')
            #
            # handle history list order -
            order = 'reverse'
            if dictionaryName == 'mmcif_img':
                order = 'forward'
            pageHtmlList = hcU.makeDictionaryIndex(downloadPath=downloadPath, dictionaryName=dictionaryName, title=tS, description=dS, authors=aS, maintainers=mS, order=order)

            subTitle = dApi.getDictionaryTitle()
            hg.writeHtmlFile('index', title='Dictionary Index', subTitle=subTitle, contentType='Index', htmlContentList=pageHtmlList)
            #
            pageHtmlList = hcU.makeCategoryGroupIndex(leadingList=leadingGroupList)
            hg.writeHtmlFile('index', title='Category Group Index', subTitle=subTitle, contentType='Groups', htmlContentList=pageHtmlList)
            groupNameList = dApi.getCategoryGroups()
            for groupName in groupNameList:
                pageHtmlList = hcU.makeCategoryGroupPage(groupName)
                hg.writeHtmlFile(groupName, title='Category Group', subTitle=groupName, contentType='Groups',
                                 htmlContentList=pageHtmlList, navBarContentType='none')

            #
            #
            pageHtmlList = hcU.makeCategoryAlphaIndex()
            hg.writeHtmlFile('index', title='Category Index', subTitle=subTitle, contentType='Categories', htmlContentList=pageHtmlList)

            pageHtmlList = hcU.makeItemCategoryAlphaIndex(openFirst=True)
            hg.writeHtmlFile('index', title='Item Index', subTitle=subTitle, contentType='Items', htmlContentList=pageHtmlList)

            pageCount = 0
            categoryNameList = dApi.getCategoryList()
            for categoryName in categoryNameList:
                pageHtmlList = hcU.makeCategoryPage(categoryName)
                hg.writeHtmlFile(categoryName, title='Data Category', subTitle=categoryName, contentType='Categories',
                                 htmlContentList=pageHtmlList, navBarContentType='none')
                pageCount += 1
                itemNameList = dApi.getItemNameList(categoryName)
                for itemName in itemNameList:
                    pageHtmlList = hcU.makeItemPage(itemName)
                    hg.writeHtmlFile(itemName, title='Data Item', subTitle=itemName, contentType='Items',
                                     htmlContentList=pageHtmlList, navBarContentType='none')
                    pageCount += 1
            logger.debug("HTML page count %d\n" % pageCount)
            #
            pageHtmlList = hcU.makeSupportingDataIndex()
            subTitle = dApi.getDictionaryTitle()
            hg.writeHtmlFile('index', title='Supporting Data', subTitle=subTitle, contentType='Data', htmlContentList=pageHtmlList)

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suiteHtmlGeneratorTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(HtmlGeneratorTests("testRenderDictionaries"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = suiteHtmlGeneratorTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
