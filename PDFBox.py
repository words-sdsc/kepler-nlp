__author__ = 'ankitgoyal'

import os
import subprocess
import sys
import codecs
import pkg_resources

__PDFBoxCommand = 'java -jar "%s" ExtractText "%s" "%s"'         #(JAR Path, PDF File Path, Text File Path)
__PDFBoxJarLocation = '/home/ankitgoyal/bioPDFX/Kepler/pdfbox-app-1.8.7.jar'

inputString = sys.stdin.readline().split(',')
pdfFileName = inputString[0].strip()
pdfFileName = os.path.abspath(pdfFileName)
txtFileName = pdfFileName.replace('.pdf', '.txt')

if not os.path.isfile(pdfFileName):
    raise Exception('"PDF Box": PDF file does not exist:', pdfFileName)

if not pdfFileName.endswith('.pdf'):
    raise Exception('"PDF Box": Not a valid PDF File:', pdfFileName, 'Please provide a PDF file')

pdfBoxCommand = __PDFBoxCommand % (__PDFBoxJarLocation, pdfFileName, txtFileName)

try:
    subprocess.check_output(pdfBoxCommand, stderr=subprocess.STDOUT, shell=True)
except:
    raise Exception('"PDF Box": Some error while running the PDF Box. Please check')

textFile = codecs.open(txtFileName, mode='r', encoding='utf-8')
pdfPageContent = textFile.read()
textFile.close()
os.remove(txtFileName)

utf8Writer = codecs.getwriter('utf8')
sys.stdout = utf8Writer(sys.stdout)
print pdfPageContent
