##
# File:    DictionaryRegistry.py
# Author:  jdw
# Date:    3-Oct-2013
# Version: 0.001
#
# Updates:
##
"""
Classes providing a registry of essential information about known data dictionaries and data item coverage statistics.

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


HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))


class DictionaryItemCoverage(object):
    """   Methods providing data item coverage with the PDB archive and chemical reference data files.
    """

    def __init__(self, dictionaryName=None, verbose=False):
        self.__verbose = verbose
        self.__debug = False
        # Name - Synonym  correspondences required to interpret coverage data -
        if dictionaryName == 'mmcif_pdbx_v40':
            baseDir = os.path.join(HERE, 'data-v4')
        else:
            baseDir = os.path.join(HERE, 'data')

        self.__pathItemAbbreviations = os.path.join(baseDir, "item_name_abbreviations.txt")
        #
        # Paths to data files with coverage statistics -
        #
        self.__pathArchiveItemCounts = os.path.join(baseDir,
                                                    "populated_column_count.txt")
        self.__pathArchiveItemCountsSpecial = os.path.join(baseDir, "populated_column_count_special.txt")
        self.__pathPrdItemCounts = os.path.join(baseDir, "prd_column_count.txt")
        self.__pathCcItemCounts = os.path.join(baseDir, "cc_column_count.txt")
        self.__pathFamilyPrdItemCounts = os.path.join(baseDir, "family_prd_column_count.txt")
        #

    def getItemCoverage(self, deliveryType='archive', specialFlag=False):
        """  Return a dictionary of usage counts for each data item for the input delivery type.

             deliveryTypes = [ 'archive', 'cc', 'prd', 'family']
        """
        if deliveryType in ['archive']:
            if specialFlag:
                return self.__getItemCounts(self.__pathArchiveItemCountsSpecial, abbrevPath=self.__pathItemAbbreviations)
            else:
                return self.__getItemCounts(self.__pathArchiveItemCounts, abbrevPath=self.__pathItemAbbreviations)
        elif deliveryType in ['cc']:
            return self.__getItemCounts(self.__pathCcItemCounts, abbrevPath=self.__pathItemAbbreviations)
        elif deliveryType in ['prd']:
            return self.__getItemCounts(self.__pathPrdItemCounts, abbrevPath=self.__pathItemAbbreviations)
        elif deliveryType in ['family']:
            return self.__getItemCounts(self.__pathFamilyPrdItemCounts, abbrevPath=self.__pathItemAbbreviations)
        else:
            return {}

    def __getItemCounts(self, itemCountsPath, abbrevPath=None):
        #
        abbrevD = {}
        if abbrevPath is not None:
            ifh = open(abbrevPath, 'r')
            for line in ifh.readlines():
                fields = [field.strip() for field in line[:-1].split()]
                itemNameReal = "_" + fields[0] + "." + fields[1]
                itemNameAbbrev = "_" + fields[0] + "." + fields[2]
                abbrevD[itemNameAbbrev] = itemNameReal
            ifh.close()
        #
        itemCountD = {}
        ifh = open(itemCountsPath, 'r')
        for line in ifh.readlines():
            if len(str(line[:-1]).strip()) < 2:
                continue
            fields = line[:-1].split()
            if len(fields) > 1:
                iCount = int(str(fields[1]))
                if iCount > 0:
                    tN = str(fields[0]).strip()
                    if tN in abbrevD:
                        it = abbrevD[tN]
                    else:
                        it = tN
                    itemCountD[it] = iCount
        ifh.close()
        #
        return itemCountD


class DictionaryRegistry(object):

    def __init__(self, verbose=False):
        self.__verbose = verbose
        self.__debug = False
        #
        self.__otherDictionaries = ['mmcif_ihm', 'mmcif_em', 'mmcif_nmr-star',
                                    'mmcif_img', 'mmcif_sas', 'mmcif_std', 'mmcif_mdb',
                                    'mmcif_biosync', 'mmcif_sym', 'mmcif_nef',
                                    ]

        self.__internalDictionaryNameList = ['mmcif_rcsb_xray', 'mmcif_rcsb_nmr', 'mmcif_pdbx_v32', 'mmcif_pdbx_v31', 'mmcif_ccp4']
        #
        self.__pdbxDictionaryNameList = ['mmcif_pdbx_v50', 'mmcif_ddl', 'mmcif_pdbx_v5_next', 'mmcif_pdbx_v40']
        self.__dictionaryNameList = []
        self.__dictionaryNameList.extend(self.__pdbxDictionaryNameList)
        self.__dictionaryNameList.extend(self.__otherDictionaries)

        self.__dictInfoD = {
            'mmcif_pdbx_v5_next': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) Development Version',
                'description': 'The development version of the PDB Exchange Dictionary',
                'maintainers': 'wwPDB',
                'developers': 'wwPDB',
                'schema': 'pdbx-v50'
            },

            'mmcif_pdbx_v5_rc': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) Version 5 (release candidate)',
                'description': 'Release candidate version V5 of the PDB Exchange Dictionary Data dictionary',
                'maintainers': 'wwPDB',
                'developers': 'wwPDB',
                'schema': 'pdbx-v50-rc'
            },

            'mmcif_pdbx_v50': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) Version 5.0 supporting the data files in the current PDB archive',
                'description': 'The current version of PDB Exchange Data Dictionary',
                'maintainers': 'wwPDB',
                'developers': 'wwPDB',
                'schema': 'pdbx-v50'
            },

            'mmcif_pdbx_v42': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) V4.2 with transitional extensions to support new features of the PDB deposition and annotation system',
                'description': 'A prior version of the PDB Exchange Data dictionary frozen at version 4.073',
                'maintainers': 'wwPDB',
                'developers': 'wwPDB',
                'schema': 'pdbx-v42',
                'dictionary': 'mmcif_pdbx_v40'
            },

            'mmcif_pdbx_v40': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) V4.0 supporting the data files in the current PDB archive',
                'description': 'A prior version of the PDB Exchange Data dictionary frozen at version 4.073',
                'maintainers': 'wwPDB',
                'developers': 'wwPDB',
                'schema': 'pdbx-v40'
            },
            'mmcif_pdbx_v32': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) supporting the content of the PDB File Format V3.2/3.15',
                'description': 'A prior version of the PDB exchange data dictionary frozen at version 1.0697',
                'maintainers': 'wwPDB',
                'schema': 'pdbx-v32'
            },
            'mmcif_pdbx_v31': {
                'title': 'PDB Exchange Dictionary (PDBx/mmCIF) supporting the content of the PDB File Format V3.1',
                'description': 'An early version of the PDB exchange data dictionary frozen at version 1.0524',
                'developers': 'wwPDB',
                'maintainers': 'wwPDB',
                'schema': None
            },
            'mmcif_std': {
                'title': 'mmCIF Dictionary',
                'description': 'Original IUCr mmCIF Dictionary',
                'developers': 'IUCr working group:  Paula M. Fitzgerald, Helen Berman,Phil Bourne, Brian McMahon, Keith Watenpaugh, and John Westbrook',
                'maintainers': 'wwPDB for the IUCr',
                'schema': 'mmcif_std'
            },
            'mmcif_ddl': {
                'title': 'DDL2 Dictionary',
                'description': 'Dictionary Description Language Version 2 supporting mmCIF and PDB Exchange Dictionary (PDBx/mmCIF)',
                'developers': 'Syd Hall and John Westbrook',
                'maintainers': 'wwPDB for the IUCr',
                'schema': 'mmcif_ddl'
            },

            'mmcif_sas': {
                'title': 'Small Angle Scattering Dictionary',
                'description': 'Draft data definitions for small-angle scattering applications ',
                'developers': 'Marc Malfois and Dmitri Svergun',
                'maintainers': 'wwPDB Small Angle Scattering Task Force',
                'schema': 'mmcif_sas'
            },

            'mmcif_nef': {
                'title': 'NMR Exchange Format Dictionary',
                'description': 'Draft data definitions for NMR exchange format definitions ',
                'developers': 'NMR Exchange Format (NEF) Working Group',
                'maintainers': 'NMR Exchange Format (NEF) Working Group',
                'schema': 'mmcif_nef'
            },

            'mmcif_em': {
                'title': '3DEM Extension Dictionary',
                'description': 'Community extension data dictionary describing 3D EM structure and experimental data to be deposited in the EMDB and PDB archives.',
                'maintainers': 'no recent updates',
                'schema': 'mmcif_em'
            },
            'mmcif_nmr-star': {
                'title': 'NMRSTAR Dictionary',
                'description': 'PDBx/mmCIF translation of the NMRSTAR data dictionary developed by the BioMagResBank',
                'developers': 'BioMagResBank',
                'maintainers': 'BioMagResBank and wwPDB',
                'schema': 'mmcif_nmr-star'
            },
            'mmcif_img': {
                'title': 'imgCIF/CBF Extension Dictionary',
                'description': 'Extension to the mmCIF dictionary describing image data collection and compact binary representation of diffraction image data',
                'developers': 'Andy Hammersley, Herbert J. Bernstein, I. David Brown, and John Westbrook',
                'maintainers': 'IUCr',
                'schema': 'mmcif_img'
            },
            'mmcif_biosync': {
                'title': 'BIOSYNC Extension Dictionary',
                'description': 'Extension to the mmCIF dictionary describing the features of synchrotron facilities and beamlines',
                'developers': 'Anne Kuller and John Westbrook',
                'maintainers': 'wwPDB',
                'schema': 'mmcif_biosync'
            },
            'mmcif_mdb': {
                'title': 'MDB Modeling Extension Dictionary',
                'description': 'Extension to the mmCIF dictionary describing homology models and homology modeling methodologies',
                'developers': 'Alexei Adzhubei and Eugenia Migliavacca',
                'maintainers': 'no recent updates',
                'schema': 'mmcif_mdb'
            },
            'mmcif_sym': {
                'title': 'Symmetry Dictionary',
                'description': 'Dictionary describing crystallographic symmetry operations',
                'developers': 'I. David Brown, Editor',
                'maintainers': 'IUCr',
                'schema': 'mmcif_sym'
            },
            'mmcif_ccp4': {
                'title': 'CCP4 Harvest Extension Dictionary',
                'description': 'Data dictionary developed for harvesting data from applications within the CCP4 system',
                'developers': 'CCP4 in collaboration with Kim Henrick.',
                'maintainers': 'no recent updates',
                'schema': 'mmcif_ccp4'
            },

            'mmcif_rcsb_nmr': {
                'title': 'RCSB PDB NMR Internal Data Dictionary',
                'description': 'Data dictionary used by RCSB PDB for internal data processing and annotation operations',
                'developers': 'RCSB PDB',
                'maintainers': 'RCSB PDB',
                'schema': None
            },

            'mmcif_rcsb_xray': {
                'title': 'RCSB PDB X-Ray Internal Data Dictionary',
                'description': 'Data dictionary used by RCSB PDB for internal data processing and annotation operations',
                'developers': 'RCSB PDB',
                'maintainers': 'RCSB PDB',
                'schema': None
            },

            'mmcif_ihm': {
                'title': 'Integrative/Hybrid (I/H) methods extension dictionary',
                'description': 'The I/H methods dictionary is an extension of the PDBx/mmCIF dictionary. This dictionary is actively developed and maintained in a github repository available at https://github.com/ihmwg/IHM-dictionary. I/H structural models that are compliant to this extension dictionary can be deposited to the PDB-Dev prototype deposition and archiving system (https://pdb-dev.wwpdb.org).',
                'developers': 'wwPDB I/H methods task force members',
                'maintainers': 'wwPDB I/H methods task force members',
                'schema': None
            },



        }

    def getDictionaryNameList(self):
        return self.__dictionaryNameList

    def getInternalDictionaryNameList(self):
        return self.__internalDictionaryNameList

    def getPdbxDictionaryNameList(self):
        return self.__pdbxDictionaryNameList

    def getPdbmlSchemaNameList(self):
        oL = ['mmcif_pdbx_v42']
        oL.extend(self.__dictionaryNameList)
        return oL

    def get(self):
        return self.__dictInfoD

    def getTitle(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]['title']
        except Exception as e:
            return None

    def getDescription(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]['description']
        except Exception as e:
            return None

    def getDevelopers(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]['developers']
        except Exception as e:
            return None

    def getMaintainers(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]['maintainers']
        except Exception as e:
            return None

    def getSchemaName(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]['schema']
        except Exception as e:
            return None