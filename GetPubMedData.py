import urllib2
import sys

__EUtils_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%s&rettype=xml"

inputString = sys.stdin.readline().split(',')
pubMedID = inputString[1].strip()
eutilsURL = __EUtils_URL % (pubMedID)
req = urllib2.Request(eutilsURL)
response = urllib2.urlopen(req)
print response.read()
