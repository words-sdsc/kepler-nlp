
from lxml import etree as XMLTree
import os
import sys

__EUtils_Title_XPath = './PubmedArticle/MedlineCitation/Article/ArticleTitle'
__EUtils__Abstract_XPath = './PubmedArticle/MedlineCitation/Article/Abstract'


def GetTextFromXMLByXPath(root, xPathString):

    xPathElement = root.find(xPathString)
    xPathText = ""

    if xPathElement is None:
        return None

    for elementText in xPathElement.itertext():
        xPathText += elementText

    return xPathText.strip()

def CorrectTitle(pdfxTree, pubMedTree):

    correctTitleString = GetTextFromXMLByXPath(pubMedTree, __EUtils_Title_XPath)
    if correctTitleString is None:
        # print '"Title Abstract Corrector": No Title in E-Utilities XML'
        return pdfxTree

    titleElement = pdfxTree.find('./article/front/title-group/article-title')
    titleParent = pdfxTree.find('./article/front/title-group')

    if titleElement is not None:
        titleParent.remove(titleElement)

    newTitleElement = XMLTree.SubElement(titleParent, 'article-title')
    newTitleElement.text = correctTitleString

    return pdfxTree


def CorrectAbstract(pdfxTree, pubMedTree):

    correctAbstractString = GetTextFromXMLByXPath(pubMedTree, __EUtils__Abstract_XPath)
    if correctAbstractString is None:
        # print '"Title Abstract Corrector": No Abstract in E-Utilities XML'
        return pdfxTree

    abstractElement = pdfxTree.find('./article/front/abstract')
    abstractParent = pdfxTree.find('./article/front')

    if abstractElement is not None:
        abstractElement.remove(abstractElement)

    abstractElement = XMLTree.SubElement(abstractParent, 'abstract')
    abstractElement.text = correctAbstractString

    return pdfxTree



def RunCorrecter(pdfxTree, pubMedTree):

    pdfxTree = CorrectTitle(pdfxTree, pubMedTree)
    pdfxTree = CorrectAbstract(pdfxTree, pubMedTree)

    return pdfxTree


def WriteResultToFile(pdfxTree, fileName):
    pdfxTree = XMLTree.tostring(pdfxTree, pretty_print=True)
    xmlFile = open(fileName, 'w')
    xmlFile.write(pdfxTree)
    xmlFile.close()


inputString = ""
for inputLine in sys.stdin:
    inputString += inputLine
inputComponents = inputString.split("\n\nAStringDelimintor\n\n")
pdfxTree = XMLTree.fromstring(inputComponents[1].strip())
pubMedTree = XMLTree.fromstring(inputComponents[4].strip())
xmlFileName = inputComponents[2].strip().split(',')[0].strip().replace('.pdf', '.xml')
pdfxTree = RunCorrecter(pdfxTree, pubMedTree)
WriteResultToFile(pdfxTree, xmlFileName)
print "Done\t"
