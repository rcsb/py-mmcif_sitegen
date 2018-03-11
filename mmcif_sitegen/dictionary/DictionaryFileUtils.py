##
# File:    DictionaryFileUtils.py
# Author:  jdw
# Date:    19-Aug-2013
# Version: 0.001
##
"""
Utility methods for accessing dictionary files.

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import sys
import os

import logging
logger = logging.getLogger(__name__)

from mmcif.io.IoAdapterPy import IoAdapterPy
from mmcif.api.DictionaryApi import DictionaryApi


class DictionaryFileUtils(object):
    """ Utility methods for accessing dictionary files.
    """

    def __init__(self, dictFilePath, verbose=False):
        """
        """
        self.__verbose = verbose
        self.__dictFilePath = dictFilePath
        #
        #  Assign the dictionary name for the input dictionary using dictionary file path.
        #
        self.__dictDirName = self.__getDictName(dictFilePath)
        #
        # Create a reference to the dictionary API -
        #
        self.__dApi = None
        #

    def __getDictName(self, dictFilePath):
        """   Extract the dictionary name from the dictioary file path.
        """
        try:
            (dirN, fN) = os.path.split(dictFilePath)
            (nm, ext) = os.path.splitext(fN)
            return nm
        except Exception as e:
            logger.error("DictionaryFileUtils.__getDictName() failed for %s\n" % dictFilePath)
            logger.exception("Failing with %s" % str(e))
        return None

    def getApi(self):
        self.__dApi = self.__getApi(dictPath=self.__dictFilePath)
        return self.__dApi

    def __getApi(self, dictPath):
        """
        """
        try:
            myIo = IoAdapterPy(verbose=self.__verbose)
            containerList = myIo.readFile(inputFilePath=dictPath)
            return DictionaryApi(containerList=containerList, consolidate=True, verbose=self.__verbose)
        except Exception as e:
            logger.error("DictionaryFileUtils.__setup() dictionary API construction failed for %s\n" % dictPath)
            logger.exception("Failing with %s" % str(e))

    def dump(self, ofh=None):
        """  Dump dictionary contents --
        """
        myOut = ofh if ofh is not None else sys.stdout

        self.__dApi.dumpCategoryIndex(fh=myOut)
        self.__dApi.dumpEnumFeatures(fh=myOut)
        self.__dApi.dumpFeatures(fh=myOut)
        self.__dApi.dumpMethods(fh=myOut)
        # self.__dApi.dumpDataSections(fh=myOut)
        self.__dApi.dumpItemLinkedGroups(fh=myOut)

if __name__ == '__main__':
    pass
