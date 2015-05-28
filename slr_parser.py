import csv
import string
import sys

class slr_parser:
	def __init__( self, dicts ):
		self.RESERVED_WORDS = dicts.getReservedWordsDict()
		self.TOKEN = dicts.getTokenDict()
		self.stack = [ 0 ]
		self.input = []
		self.LRTable = []
		self.gr = self.grammar()
		with open( 'lrTable.csv', 'rb' ) as csvFile:
			reader = csv.DictReader( csvFile, delimiter = ',' )
			for row in reader:
				self.LRTable.append( row )
		
		for row in self.LRTable:
			print row
		print self.LRTable[ 0 ][ 'int' ]

	def run( self, tokens ):
		self.tokens = tokens
		keys = self.TOKEN.keys()
		values = self.TOKEN.values()
		for expr in tokens:
			for code, raw in expr:
				tokenTry = values.index( code )
				#print keys[ tokenTry ]
				#self.input.append( keys[ tokenTry ] )
				self.input.append( raw )
		self.input.append( '$' )
		print "INPUT IS: ", self.input
		print self.printList( self.input )
		action = ""
		while action != "acc":
			try:
				action = self.LRTable[ int( self.stack[ -1 ] ) ][ self.input[ 0 ] ]

				print "\nStack: ", self.printList( self.stack )
				print "Input: ", self.printList( self.input )
				print "Action: ", action

				if action[ 0 ] == 's':
					self.stack.append( self.input.pop( 0 ) )
					self.stack.append( int( action[ 1: ] ) )
				elif action[ 0 ] == 'r':
					left, right = self.gr[ int( action[ 1: ] ) ].split( '->' )
					left = string.replace( left, " ", "" )
					rightList = right.split()

					rightList.reverse()
					print "Rule: ", rightList
					for token in rightList:
						print "Stack: ", self.stack
						self.stack.pop()
						if self.stack[ -1 ] != token:
							print "Error at parsing: ", token, " expected. ", self.stack[ -1 ], " gotten."
							self.error()
						else:
							self.stack.pop()
					latestState = int( self.stack[ -1 ] )
					stateToAppend = self.LRTable[ latestState ][ left ]
					self.stack.append( left )
					self.stack.append( stateToAppend )
				elif action == 'acc':
					print "Done"
					break

			except KeyError, e:
				self.error()
				sys.exit( "Leaving program." )
				break

	def error( self ):
		print "fuck error"

	def grammar( self ):
		gr = dict()

		gr[ 0 ] = "program -> declaration-list"
		gr[ 1 ] = "declaration-list -> declaration-list declaration"
		gr[ 2 ] = "declaration-list -> declaration"
		gr[ 3 ] = "declaration -> var-declaration"
		gr[ 4 ] = "var-declaration -> type-specifier var-decl-list ;"
		gr[ 5 ] = "scoped-var-declarations -> scoped-type-specifier var-decl-list ;"
		gr[ 6 ] = "scoped-type-specifier -> static type-specifier"
		gr[ 7 ] = "scoped-type-specifier -> type-specifier"
		gr[ 8 ] = "type-specifier -> int"
		gr[ 9 ] = "type-specifier -> bool"
		gr[ 10 ] = "type-specifier -> char"
		gr[ 11 ] = "var-decl-list -> var-decl-list , var-decl-initialize"
		gr[ 12 ] = "var-decl-list -> var-decl-initialize"
		gr[ 13 ] = "var-decl-initialize -> var-decl-id"
		gr[ 14 ] = "var-decl-initialize -> var-decl-id = simple-expression"
		gr[ 15 ] = "var-decl-id -> ID"
		gr[ 16 ] = "simple-expression -> and-expression"
		gr[ 17 ] = "and-expression -> unary-rel-expression"
		gr[ 18 ] = "unary-rel-expression -> rel-expression"
		gr[ 19 ] = "rel-expression -> sum-expression"
		gr[ 20 ] = "sum-expression -> sum-expression sumop term"
		gr[ 21 ] = "sum-expression -> term"
		gr[ 22 ] = "sumop -> +"
		gr[ 23 ] = "sumop -> -"
		gr[ 24 ] = "term -> term mulop unary-expression"
		gr[ 25 ] = "term -> unary-expression"
		gr[ 26 ] = "mulop -> *"
		gr[ 27 ] = "mulop -> /"
		gr[ 28 ] = "mulop -> %"
		gr[ 29 ] = "unary-expression -> unaryop unary-expression"
		gr[ 30 ] = "unary-expression -> factor"
		gr[ 31 ] = "factor -> immutable"
		gr[ 32 ] = "factor -> mutable"
		gr[ 33 ] = "unaryop -> -"
		gr[ 34 ] = "unaryop -> *"
		gr[ 35 ] = "mutable -> ID"
		gr[ 36 ] = "immutable -> constant"
		gr[ 37 ] = "constant -> NUMCONS"

		return gr

	def printList( self, arr ):
		get = ""
		for ele in arr:
			get = get + str( ele ) + " "
		return get