import sys
import re
import io
from dictionaries import dictionaries
from lexical_analyser import lexical_analyser
from slr_parser import slr_parser

class ProgLang:
	def __init__( self, inFileName, outFileName = "a.out" ):
		# lexical: lexical analyser: feed raw input and output lexemes
		# syntax: syntax analyser: feed lexemes and output syntactical structure
		# semantic: semantics analyser: feed syntactical structure and apply meaning and execute
		self.dicts = dictionaries()
		self.lexical = lexical_analyser( inFileName, self.dicts )
		self.parser = slr_parser( self.dicts )
		#self.semantic = SemanticsAnalyser()
		self.runProgram()

	def runProgram( self ):
		# insert logic for running program here
		self.tokens = self.lexical.run()
		self.parsed = self.parser.run( self.tokens )
		for row in self.parsed:
			print row

progLang = ProgLang( sys.argv[ 1 ] )
