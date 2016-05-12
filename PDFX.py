__author__ = 'ankitgoyal'

import os
import subprocess
import sys
from lxml import etree as XMLTree


__PDFxUrlPath = 'http://pdfx.cs.man.ac.uk'
__PDFxCurlCommand = 'curl --data-binary @"%s" -H "Content-Type: application/pdf" -L "%s" > "%s"'        #(PDF File Name, PDFX URL, XML File Name)


inputString = sys.stdin.readline().split(',')
pdfFileName = inputString[0].strip()
pdfFileName = os.path.abspath(pdfFileName)
xmlFileName = pdfFileName.replace('.pdf', '.xml')
xmlFileData = None


def StripUselessTagsFromXML():
    uselessTagsList = ['h1','disp-formula', 'marker','meta','xref', 'aff','tr','tbody','label','h2',
                    'th','td','thead','ref','email','job','doi','name','base_name','ext-link',
                    'caption','s','warning','image','tfoot']

    for uselessTags in uselessTagsList:
        XMLTree.strip_tags(xmlFileData, uselessTags)


def StripOtherSmallTagsFromXML():
    for xmlNode in xmlFileData.iter():
        xmlNodeText = xmlNode.text

        descendentsCount = sum([1 for xmlDescendents in xmlNode.getchildren()])

        if xmlNodeText != None and len(xmlNodeText.split()) < 15 and descendentsCount == 0:
            XMLTree.strip_tags(xmlFileData, xmlNode)



if not os.path.isfile(pdfFileName):
    raise Exception('"PDFx": PDF file does not exist:', pdfFileName)

if not pdfFileName.endswith('.pdf'):
    raise Exception('"PDFx": Not a valid PDF File:', pdfFileName, 'Please provide a PDF file')

pdfxCommand = __PDFxCurlCommand % (pdfFileName, __PDFxUrlPath, xmlFileName)

try:
    retVal = subprocess.check_output(pdfxCommand, stderr=subprocess.STDOUT, shell=True)
except:
    raise Exception('"PDFx": Some error while running the PDFx. Please check')

if not os.path.isfile(xmlFileName):
    raise Exception('"PDFx": Some error while running PDFx. Output could not be stored.')

xmlFileData = XMLTree.parse(xmlFileName)

StripUselessTagsFromXML()
StripOtherSmallTagsFromXML()

os.remove(xmlFileName)
print XMLTree.tostring(xmlFileData.getroot())
