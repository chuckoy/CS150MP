import sys
import re
import io

class LexicalAnalyser:
	def __init__( self, inFileName ):
		self.inFileName = inFileName

	# open file and parse. so far will only read line-by-line until EOF.
	# change this to read word-for-word; if word is not recognised, proceed to char-by-char analysis
	def run:
		with open( self.inFileName, 'r' ) as inputFile:
			while True:
				line = inputFile.readline()
				if not line:
					print( "EOF reached" )
					break