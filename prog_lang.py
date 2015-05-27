import sys
import re
import io
from lexical_analyser import lexical_analyser
from dictionaries import dictionaries

class ProgLang:
	def __init__( self, inFileName, outFileName = "a.out" ):
		# lexical: lexical analyser: feed raw input and output lexemes
		# syntax: syntax analyser: feed lexemes and output syntactical structure
		# semantic: semantics analyser: feed syntactical structure and apply meaning and execute
		self.dicts = dictionaries()
		self.lexical = lexical_analyser( inFileName, self.dicts )
		#self.parser = SLRParser( inFileName, self.dicts )
		#self.semantic = SemanticsAnalyser()
		self.runProgram()

	def runProgram( self ):
		# insert logic for running program here
		self.tokens = self.lexical.run()
		print self.tokens
		#self.parser.run( self.tokens )

progLang = ProgLang( sys.argv[ 1 ] )
