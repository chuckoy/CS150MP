import csv
import string
import sys

class slr_parser:
	def __init__( self, dicts ):
		"""	Constructor
		:param dicts: utility file for dictionaries
		"""
		# initialise needed variables
		self.RESERVED_WORDS = dicts.getReservedWordsDict()
		self.TOKEN = dicts.getTokenDict()
		self.stack = [ 0 ]
		self.input = []
		self.LRTable = []

		# generate grammar for rule reduction
		self.gr = self.grammar()

		# read the csv file containing the parse table and create
		with open( 'lrTable.csv', 'rb' ) as csvFile:
			reader = csv.DictReader( csvFile, delimiter = ',' )
			for row in reader:
				self.LRTable.append( row )
		# the lrtable is a list of dictionaries
		# the ith index represents the ith state of the automata

	def run( self, tokens ):
		"""
		Returns a list of lists of lists.
		One outermost list containing all expressions.
		Each middle list is one expression.
		The innermost list is the pair ( unprocessed_input, token )
		"""
		# split the tokens
		self.tokens = tokens
		keys = self.TOKEN.keys()
		values = self.TOKEN.values()

		# fill the input with the processed feed
		for expr in tokens:
			print expr
			for code, proc, raw in expr:
				#print code
				#print values
				#print keys
				tokenTry = values.index( code )
				self.input.append( proc )
		# append $ to notify end of feed
		self.input.append( '$' )

		# while action is not accept, keep resolving
		action = ""
		while action != "acc":
			try:
				print self.stack
				action = self.LRTable[ int( self.stack[ -1 ] ) ][ self.input[ 0 ] ]

				print "\nStack: ", self.printList( self.stack )
				print "Input: ", self.printList( self.input )
				print "Action: ", action

				# perform a shift action
				if action[ 0 ] == 's':
					self.stack.append( self.input.pop( 0 ) )
					self.stack.append( int( action[ 1: ] ) )

				# perform a reduction
				elif action[ 0 ] == 'r':
					left, right = self.gr[ int( action[ 1: ] ) ].split( '->' )
					left = string.replace( left, " ", "" )
					rightList = right.split()

					# get the rule and reverse to check
					rightList.reverse()
					for token in rightList:
						# pop the state number at the top of the stack
						self.stack.pop()
						# if the token received is not the expected token
						if self.stack[ -1 ] == token:
							# pop the token for reduction purposes
							self.stack.pop()
						elif token == "\'\'":
							self.stack.pop()
						else:
							print "Error at parsing: ", token, " expected. ", self.stack[ -1 ], " gotten."
							self.error()
					# find the proper GOTO and append the correct state number
					latestState = int( self.stack[ -1 ] )
					stateToAppend = self.LRTable[ latestState ][ left ]
					self.stack.append( left )
					self.stack.append( stateToAppend )

				# finished parsing; process output properly
				elif action == 'acc':
					print "Done"
					response = []
					for expr in tokens:
						subResponse = []
						for code, proc, raw in expr:
							tokenTry = values.index( code )
							subResponse.append( [ raw, keys[ tokenTry ] ] )
						response.append( subResponse )
					break

			# key error in parse table or grammar
			except KeyError, e:
				print "KEYERROR FK"
				print self.input
				self.error()
				break
		return response

	def error( self ):
		"""
		Error handling function
		"""
		print "Error"
		sys.exit( "Leaving program." )

	def grammar( self ):
		"""
		Returns dictionary as: (ruleNumber, rule) pair
		"""
		gr = dict()
		i = 0
		with open( "grammar.txt", 'r' ) as grammarFile:
			for rule in grammarFile:
				gr[ i ] = rule.rstrip()
				i += 1
		return gr
		"""
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
		"""

	def printList( self, arr ):
		"""
		Function for printing from stack and input lists
		"""
		get = ""
		for ele in arr:
			get = get + str( ele ) + " "
		return get
