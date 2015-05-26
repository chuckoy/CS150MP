import sys
import re
import io

class ProgLang:
	def __init__( self, inFileName, outFileName = "a.out" ):
		# lexical: lexical analyser: feed raw input and output lexemes
		# syntax: syntax analyser: feed lexemes and output syntactical structure
		# semantic: semantics analyser: feed syntactical structure and apply meaning and execute
		self.parser = RecursiveDescent( self.inFileName )
		self.semantic = SemanticsAnalyser()
		self.runProgram()

	def runProgram():
		# insert logic for running program here
		self.lexical.run()

if( sys.argv[ 2 ] ):
	outFileName = sys.argv[ 2 ]
progLang = ProgLang( sys.argv[ 1 ] )
