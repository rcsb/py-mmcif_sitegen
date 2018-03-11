##
# File:    HtmlMarkupUtils.py
# Author:  jdw
# Date:    19-Aug-2013
# Version: 0.001
##
"""
Utility methods for creating HTML markup.

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import sys
import os
import re
import copy
from itertools import cycle


import logging
logger = logging.getLogger(__name__)


class HtmlMarkupUtils(object):
    """ Utility methods for creating markup form indivdual HTML elements.
    """
    _html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    def __init__(self, verbose=False):
        """
        """
        self.__verbose = verbose

    def html_escape(self, text):
        """Produce entities within text."""
        return "".join(HtmlMarkupUtils._html_escape_table.get(c, c) for c in text)

    def escapeText(self, inputText, format='ascii', markupMath=False):
        if inputText is None:
            return ''
        if format == 'ascii':
            inputText = self.html_escape(inputText)
            if markupMath:
                inputText = self.__replaceDelimiters(inputText, delimiter='~', alternateMarkup=['<sub>', '</sub>'])
                inputText = self.__replaceDelimiters(inputText, delimiter='\^', alternateMarkup=['<sup>', '</sup>'])
            return inputText
        else:
            return inputText

    def __replaceDelimiters(self, inputString, delimiter='~', alternateMarkup=['<sub>', '</sub>']):
        a = cycle(alternateMarkup)
        return re.sub(delimiter, lambda x: next(a), inputString)

    def getFormatted(self, inputText, wrapper='pre', format='ascii', markupMath=False, addLeadingSpace=True):
        """
        """
        if addLeadingSpace:
            lS = ' '
        else:
            lS = ''

        if markupMath:
            inputText = self.escapeText(inputText, format='ascii')
            inputText = self.__replaceDelimiters(inputText, delimiter='~', alternateMarkup=['<sub>', '</sub>'])
            inputText = self.__replaceDelimiters(inputText, delimiter='\^', alternateMarkup=['<sup>', '</sup>'])
            wrapper = 'verbatim'
            format = 'html'

        if format == 'ascii':
            if wrapper == 'pre':
                html = '<pre class="pre-scrollable">%s%s</pre>' % (lS, self.escapeText(inputText))
            elif wrapper == 'code':
                html = '<code>%s%s</code>' % (lS, self.escapeText(inputText))
            elif wrapper == 'verbatim':
                inputText = inputText.replace('\n', '<br />')
                html = '<div class="my-monospace highlight">%s%s</div>' % (lS, self.escapeText(inputText))
            else:
                html = '<div class="my-monospace">%s%s</div>' % (lS, self.escapeText(inputText))
        else:
            if wrapper == 'pre':
                html = '<pre class="pre-scrollable">%s%s</pre>' % (lS, inputText)
            elif wrapper == 'code':
                html = '<code>%s%s</code>' % (lS, inputText)
            elif wrapper == 'verbatim':
                #inputText = inputText.replace('\n','<br />')
                html = '<div class="my-monospace higlight">%s%s</div>' % (lS, inputText)
            else:
                html = '<div class="my-monospace highlight">%s%s</div>' % (lS, inputText)
        return html

    def getAnchor(self, contentUrl, contentLabel, cssClassString=None, format="ascii"):
        label = self.escapeText(inputText=contentLabel, format=format)
        if cssClassString is None:
            html = '<a href="%s">%s</a>' % (contentUrl, label)
        else:
            html = '<a href="%s" class="%s">%s</a>' % (contentUrl, cssClassString, label)
        #
        return html

    def getGlyphAnchor(self, tipText, glyphPath, cssClass='pull-right', imageCssClass=''):
        return '<a href="#" class="mytip %s" data-toggle="tooltip"  data-placement="left" title="%s"> <img class="%s" src="%s"></a>' % (cssClass, tipText, imageCssClass, glyphPath)

    def getButtonAnchor(self, contentLabel, url="#", format="ascii", cssClassAdd="btn-lg btn-primary", dataAttributes=''):
        label = self.escapeText(inputText=contentLabel, format=format)
        return '<a %s class="btn %s" href="%s">%s</a>' % (dataAttributes, cssClassAdd, url, label)

    def addModalButtonTrigger(self, contentLabel, format='ascii', modalId=None, cssClassAdd='btn-primary btn-lg'):
        """
        """
        label = self.escapeText(inputText=contentLabel, format=format)
        return '<a data-toggle="modal" href="#%s" class="btn %s">%s</a>' % (modalId, cssClassAdd, label)

    def getImage(self, src, altText, width, height, cssClassAdd=''):
        return '<img src="%s" width=%s height=%s alt="%s" class="%s">' % (src, altText, width, height, cssClassAdd)

    def getBadge(self, badgeText, addClass=None):
        if addClass is not None:
            return '<span class="badge %s ">%s</span>' % (badgeText, addClass)
        else:
            return '<span class="badge">%s</span>' % badgeText

    def getIndexTitle(self, title):
        # return '<h3> - &nbsp;%s &nbsp; - </h3>' % title
        return '-&nbsp;%s &nbsp;-' % title


class HtmlComponentMarkupUtils(object):
    """ Utility methods for creating markup for HTML components such as tables, panels,
        accordions, list-groups, description lists, ...

    """

    def __init__(self, verbose=False):
        """
        """
        self.__verbose = verbose
        self.__oL = []
        self.__mU = HtmlMarkupUtils(verbose=self.__verbose)

    def getHtmlList(self):
        """ Return a copy of the state of the generated HTML.
        """
        return copy.deepcopy(self.__oL)

    def clear(self):
        self.__oL = []

    def beginContainer(self, type='row'):
        self.__oL.append('<div class="%s">' % type)

    def endContainer(self):
        self.__oL.append('</div>')

    def addContent(self, htmlList):
        self.__oL.extend(htmlList)

    def beginPanel(self, title, style='panel-default', format='ascii'):
        self.__oL.append('<div class="panel %s">' % style)
        self.__oL.append('<div class="panel-heading">')
        val = self.__mU.escapeText(title, format=format)
        self.__oL.append('<h3 class="panel-title">%s</h3>' % val)
        self.__oL.append('</div>')
        self.__oL.append('<div class="panel-body">')

    def endPanel(self):
        self.__oL.append('</div>')
        self.__oL.append('</div>')

    def beginTable(self, columnNameList, style='default', format='ascii'):
        #
        self.__curTableColumnCount = len(columnNameList)
        self.__oL.append('<div class="my-table-scrollable">')
        self.__oL.append('<table class="table table-striped table-condensed ">')
        self.__oL.append('<thead>')
        self.__oL.append('<tr>')
        for colName in columnNameList:
            val = self.__mU.escapeText(colName, format=format)
            self.__oL.append('<th>%s</th>' % val)
        self.__oL.append('</tr>')
        self.__oL.append('</thead>')
        self.__oL.append('<tbody>')

    def addTableRow(self, rowValueList, format='ascii', newLines='verbatim', markupMath=False):
        self.__oL.append('<tr>')
        for rowValue in rowValueList:
            val = self.__mU.escapeText(rowValue, format=format, markupMath=markupMath)

            if newLines == 'verbatim':
                tV = val.replace('\n', '<br />')
                self.__oL.append('<td class="my-monospace">%s</td>' % tV)
            else:
                self.__oL.append('<td>%s</td>' % val)

        self.__oL.append('</tr>')

    def endTable(self):
        self.__oL.append('</tbody>')
        self.__oL.append('</table>')
        self.__oL.append('</div>')

    def beginDescriptionList(self, style='default'):
        if style in ['default']:
            self.__oL.append('<dl class="dl-horizontal dl-lg">')
        else:
            self.__oL.append('<dl class="dl-lg">')

    def addDescription(self, termSt, descriptionSt, formatTerm='ascii', formatDescription='ascii', cssClassTerm=None, cssClassDescription=None, extraSpace=False):

        tVal = self.__mU.escapeText(termSt, format=formatTerm)
        dVal = self.__mU.escapeText(descriptionSt, format=formatDescription)

        if cssClassTerm is not None:
            cssT = ' class="%s" ' % cssClassTerm
        else:
            cssT = ''

        if cssClassDescription is not None:
            cssD = ' class="%s" ' % cssClassDescription
        else:
            cssD = ''

        self.__oL.append('<dt %s >%s</dt>' % (cssT, tVal))
        self.__oL.append('<dd %s >%s</dd>' % (cssD, dVal))
        if (extraSpace):
            self.__oL.append('<br />')

    def endDescriptionList(self):
        self.__oL.append('</dl>')

    def beginAccordionPanelGroup(self, panelGroupId='1'):
        self.__oL.append('<div class="panel-group my-spacer" id="%s">' % panelGroupId)

    def endAccordionPanelGroup(self):
        self.__oL.append('</div> <!-- end accordion panel group -->')

    def addAccordionPanel(self, title='myPanel', subTitle=None, panelTextList=[], panelId='1', panelGroupId='1', openFlag=False, toggleText='(view/hide)', topId=None):

        op = 'in' if openFlag else ''
        if topId is not None:
            self.__oL.append('<div id="%s" class="panel panel-default"> <!-- begin top accordion panel -->' % topId)
        else:
            self.__oL.append('<div class="panel panel-default"> <!-- begin top accordion panel -->')

        self.__oL.append('   <div class="panel-heading">')
        self.__oL.append('       <div class="row">')
        if subTitle is None:
            self.__oL.append('          <div class="col-md-8">')
            self.__oL.append('	             <h4 class="panel-title"> %s </h4> ' % title)
            self.__oL.append('          </div>')
            self.__oL.append('          <div class="col-md-4">')
            self.__oL.append('              <a class="accordion-toggle pull-right" data-toggle="collapse" data-parent="#%s" href="#%s">' % (panelGroupId, panelId))
            self.__oL.append(' %s' % (toggleText))
            self.__oL.append('              </a>')
            self.__oL.append('           </div>')
        else:
            self.__oL.append('          <div class="col-md-3">')
            self.__oL.append('	             <h4 class="panel-title"> %s </h4> ' % title)
            self.__oL.append('          </div>')
            self.__oL.append('          <div class="col-md-5">')
            self.__oL.append('	            <h4 class="panel-title"> %s </h4> ' % subTitle)
            self.__oL.append('          </div>')

            self.__oL.append('          <div class="col-md-4">')
            self.__oL.append('             <a class="accordion-toggle pull-right" data-toggle="collapse" data-parent="#%s" href="#%s">' % (panelGroupId, panelId))
            self.__oL.append(' %s' % (toggleText))
            self.__oL.append('             </a>')
            self.__oL.append('          </div>')
        self.__oL.append('       </div> <!-- end heading row -->')
        self.__oL.append('   </div> <!-- end panel heading -->')

        self.__oL.append('    <div id="%s" class="panel-collapse collapse %s">' % (panelId, op))
        self.__oL.append('      <div class="panel-body">')
        self.__oL.append('<!-- BEGIN inserted markup -->')
        self.__oL.extend(panelTextList)
        self.__oL.append('<!-- END inserted markup -->')
        self.__oL.append('      </div> <!-- end panel body-->')
        self.__oL.append('    </div> <!-- end panel-collapse -->')
        self.__oL.append('</div> <!-- end top accordion panel panel-default -->')

    def beginLinkListGroup(self):
        self.__oL.append('<div class="list-group">')

    def addLinkListItem(self, linkUrl, linkValue, format='ascii', active=False):
        aF = 'active' if active else ''
        val = self.__mU.escapeText(listValue, format=format)
        self.__oL.append('<a href="%s" class="list-group-item %s">%s</a>' % (linkUrl, aF, val))

    def addLinkListItem(self, linkUrl, linkValue, format='ascii', active=False):
        aF = 'active' if active else ''
        val = self.__mU.escapeText(listValue, format=format)
        self.__oL.append('<a href="%s" class="list-group-item %s">%s</a>' % (linkUrl, aF, val))

    def endLinkListGroup(self):
        self.__oL.append('</div>')

    def beginListGroup(self):
        self.__oL.append('<ul class="list-group">')

    def addListItem(self, listItem, format='ascii', active=False, cssClass=''):
        aF = 'active' if active else ''
        val = self.__mU.escapeText(listItem, format=format)
        self.__oL.append('<li class="list-group-item %s %s">%s</li>' % (aF, cssClass, val))

    def endListGroup(self):
        self.__oL.append('</ul>')

    def beginInLineList(self):
        self.__oL.append('<ul class="list-inline">')

    def addInLineListItem(self, listItem, format='ascii', cssClass=''):
        val = self.__mU.escapeText(listItem, format=format)
        self.__oL.append('<li class="%s">%s</li>' % (cssClass, val))

    def addInLineList(self, itemList, format='ascii', cssClass=''):
        for listItem in itemList:
            val = self.__mU.escapeText(listItem, format=format)
            self.__oL.append('<li class="%s">%s</li>' % (cssClass, val))

    def endInLineList(self):
        self.__oL.append('</ul>')

    def addModalImageDialog(self, modalId=None, modalTitle='', imagePath='', imageText='', cssModalSect='my-image-scrollable', cssModalClose='btn-wwpdb-green'):
        """
            Template markup --
            <!-- Button trigger modal -->
            <a data-toggle="modal" href="#myModal" class="btn btn-primary btn-lg">Launch demo modal</a>
            <a data-toggle="modal" href="#myModal" class="btn btn-primary btn-lg"><img src="figure-icon.svg" width=70 height=70 alt="my image" class="img-thumbnail"></a> some related text

            <!-- Modal -->
            <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
              <div class="my-modal-dialog">
                  <div class="modal-content">
                     <div class="modal-header">
                         <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                         <h4 class="modal-title">Category Diagram</h4>
                     </div>
                     <div class="modal-body">
                          <div class="row my-image-scrollable">
                             <object type="image/svg+xml" data="entity_neighbors.svg" border="1"></object>
                          </div>
                     </div>
                     <div class="modal-footer">
                         <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                     </div>
                  </div><!-- /.modal-content -->
              </div><!-- /.modal-dialog -->
           </div><!-- /.modal -->
        """
        self.__oL.append('<div class="modal fade" id="%s" tabindex="-1" role="dialog" aria-labelledby="%sLabel" aria-hidden="true">' % (modalId, modalId))
        self.__oL.append('    <div class="my-modal-dialog">')
        self.__oL.append('        <div class="modal-content">')
        self.__oL.append('            <div class="modal-header">')
        self.__oL.append('                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>')
        self.__oL.append('                         <h4 class="modal-title">%s</h4>' % modalTitle)
        self.__oL.append('            </div>')
        self.__oL.append('            <div class="modal-body">')
        self.__oL.append('                  <div class="row %s">' % cssModalSect)
        #  using object and image  tags was unsatisfactory -
        #self.__oL.append('                       <object type="image/svg+xml" data="%s" border="1"></object>' % imagePath)
        #self.__oL.append('                       <iframe class="my-image-iframe" width="100%s" height="700" src="%s"></iframe>'  % ('%',imagePath))
        self.__oL.append('                       <iframe class="my-iframe-handle" src="%s"></iframe>' % (imagePath))
        self.__oL.append('                  </div>')
        self.__oL.append('            </div>')
        self.__oL.append('            <div class="modal-footer">')
        self.__oL.append('                <button type="button" class="btn %s" data-dismiss="modal">Close</button>' % cssModalClose)
        self.__oL.append('            </div>')
        self.__oL.append('       </div><!-- /.modal-content -->')
        self.__oL.append('   </div><!-- /.modal-dialog -->')
        self.__oL.append('</div><!-- /.modal -->')


if __name__ == '__main__':
    pass
