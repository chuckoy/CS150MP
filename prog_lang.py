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
		keys = self.dicts.getTokenDict().keys()
		values = self.dicts.getTokenDict().values()

		# insert logic for running program here
		self.tokens = self.lexical.run()
		self.parsed = self.parser.run( self.tokens )
		hotfix = []
		for expr in self.tokens:
			subHotfix = []
			for code, proc, raw in expr:
				tokenTry = values.index( code )
				subHotfix.append( [ raw, keys[ tokenTry ] ] )
			hotfix.append( subHotfix )

progLang = ProgLang( sys.argv[ 1 ] )
