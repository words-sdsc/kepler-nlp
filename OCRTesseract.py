__author__ = 'ankitgoyal'

import os
import subprocess
import sys
import re
import codecs
from multiprocessing import Pool


__ConvertImageDensity = 200
__ConvertMaxRAMUsage = 8
__ConvertMaxArea = 10

__ImageMagickCommand = '/opt/local/bin/convert -monitor -colorspace gray -limit memory %dGiB -limit area %dGiB -density %d "%s" -quality 100 "%s"'         # (Max RAM Usage, Max Area Usage, Image Density, PDF File Name, Image File Name)
__TesseractCommand = '/opt/local/bin/tesseract "%s" "%s" -l ell+spsymbols+eng'     # (Image File Name, Output File Name)

inputString = sys.stdin.readline().split(',')
pdfFileName = inputString[0].strip()
pdfFileName = os.path.abspath(pdfFileName)
imgFileName = pdfFileName.replace('.pdf', '.jpg')
txtFileName = pdfFileName.replace('.pdf', '_OCR.txt')


def ConvertPDFPagestoImages():
    if not os.path.isfile(pdfFileName):
        raise Exception('"OCR": PDF file does not exist:', pdfFileName)

    if not pdfFileName.endswith('.pdf'):
        raise Exception('"OCR": Not a valid PDF File:', pdfFileName, 'Please provide a PDF file')

    imageMagickCommand = __ImageMagickCommand % (__ConvertMaxRAMUsage, __ConvertMaxArea, __ConvertImageDensity, pdfFileName, imgFileName)

    try:
    	retVal = subprocess.check_output(imageMagickCommand, stderr=subprocess.STDOUT, shell=True)
    except:
        raise Exception('"OCR": Some error while running the ImageMagick. Please check')

    directoryPath = os.path.dirname(pdfFileName)
    fileName = os.path.basename(pdfFileName)
    imageFileList = [imageFileName for imageFileName in os.listdir(directoryPath) if fileName.replace('.pdf','') in imageFileName and ".jpg" in imageFileName]

    if len(imageFileList) == 0:
        raise Exception('"OCR": Some error while running ImageMagick. Output could not be stored.')


    imageFileNameList = [os.path.join(directoryPath, fileName.replace('.pdf','') + '-' + str(index) + ".jpg") for index,_ in enumerate(imageFileList)]
    pdfPageTextList = Pool(processes = 1).map(GetPDFTextUsingOCR, imageFileNameList)
    pdfTextString = ''.join(pdfPageTextList)

    utf8Writer = codecs.getwriter('utf8')
    sys.stdout = utf8Writer(sys.stdout)
    print pdfTextString


def GetPDFTextUsingOCR(imageFileName):

    pageNumber = int(re.findall('\w*-(\d+).jpg', imageFileName)[0])

    tesseractCommand = __TesseractCommand % (imageFileName, imageFileName.replace('.jpg', ''))
    try:
        subprocess.check_output(tesseractCommand, stderr=subprocess.STDOUT, shell=True)
    except:
        os.remove(imageFileName)
        return None

    textFileName = imageFileName.replace('.jpg','.txt')
    textFile = codecs.open(textFileName, mode='r', encoding='utf-8')
    pdfPageContent = textFile.read()
    textFile.close()

    os.remove(textFileName)
    os.remove(imageFileName)

    return pdfPageContent

ConvertPDFPagestoImages()
