import sys

inputFileName = sys.argv[1]
for fileLine in open(inputFileName, 'r'):
	print fileLine.strip()

