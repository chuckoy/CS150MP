class lexical_analyser:
	def __init__( self, inFileName, dicts ):
		"""	Constructor
		:param inFileName:  name of input file
		:param resWords: reservedWords class instance
		""" 
		self.lexeme = []
		self.charClass = 0
		self.nextChar = ''
		self.inFileName = inFileName
		# character classes
		self.CHAR_CLASSES = {	'EOF' : -1,	
								'LETTER' : 0,
								'DIGIT' : 1,
								'ADD' : 2,
								'SUB' : 3,
								'DOT' : 80,
								'SINGLE_QUOTE' : 81,
								'UNKNOWN' : 99 }
		self.RESERVED_WORDS = dicts.getReservedWordsDict()
		self.TOKEN = dicts.getTokenDict()

	def run( self ):
		"""
		Returns a list of the tokens from the given inFileName in the constructor
		"""
		tokens = []
		currExpr = []
		with open( self.inFileName, 'r' ) as self.in_fp:
			while self.charClass != self.CHAR_CLASSES[ 'EOF' ]:
				currExpr.append( self.lex() )
				if self.nextToken == self.TOKEN[ 'SEMICOLON' ]:
					tokens.append( currExpr )
					currExpr = []
		#tokens.append( [ ( -1, "EOF" ) ] )
		return tokens

	def error( self, receivedNum, expectedNum ):
		"""	Error handling function
		:param receivedNum: The received charClass
		:param expectedNum: Expected charClass
		"""
		chKeys = self.CHAR_CLASSES.keys()
		chValues = self.CHAR_CLASSES.values()
		charClassExp = chValues.index( expectedNum )
		charClassRec = chValues.index( receivedNum )
		print "Error tokenising: ", chKeys[ charClassExp ], " expected. ", chKeys[ charClassRec ], " received."
		sys.exit( "Leaving program" )

	def getChar( self ):
		"""
		Get a character and assign the proper charClass
		"""
		self.nextChar = self.in_fp.read( 1 )
		if self.nextChar:
			if self.nextChar.isalpha():
				self.charClass = self.CHAR_CLASSES[ 'LETTER' ]
			elif self.nextChar.isdigit():
				self.charClass = self.CHAR_CLASSES[ 'DIGIT' ]
			elif self.nextChar == '+':
				self.charClass = self.CHAR_CLASSES[ 'ADD' ]
			elif self.nextChar == '-':
				self.charClass = self.CHAR_CLASSES[ 'SUB' ]
			elif self.nextChar == '.':
				self.charClass = self.CHAR_CLASSES[ 'DOT' ]
			elif self.nextChar == '\'':
				self.charClass = self.CHAR_CLASSES[ 'SINGLE_QUOTE' ]
			else:
				self.charClass = self.CHAR_CLASSES[ 'UNKNOWN' ]
		else:
			self.charClass = self.CHAR_CLASSES[ 'EOF' ]

	def addChar( self ):
		"""
		Append the character to the current lexeme (for tracking)
		"""
		self.lexeme.append( self.nextChar )
		self.lexeme2.append( self.nextChar )

	def lookup( self, ch ):
		""" Looks up unknown chars (not digit nor letter). Returns token type
		:param ch: the char that is being looked up
		"""
		self.addChar()
		if ch == '(':
			self.nextToken = self.TOKEN[ 'LEFT_PAREN' ]
		elif ch == ')':
			self.nextToken = self.TOKEN[ 'RIGHT_PAREN' ]
		elif ch == '*':
			self.nextToken = self.TOKEN[ 'MULT_OP' ]
		elif ch == '/':
			self.nextToken = self.TOKEN[ 'DIV_OP' ]
		elif ch == '=':
			self.nextToken = self.TOKEN[ 'ASSIGN_OP' ]
		elif ch == ';':
			self.nextToken = self.TOKEN[ 'SEMICOLON' ]
		elif ch == '{':
			self.nextToken = self.TOKEN[ 'LEFT_CURLY' ]
		elif ch == '}':
			self.nextToken = self.TOKEN[ 'RIGHT_CURLY' ]
		elif ch == '.':
			self.nextToken = self.TOKEN[ 'DOT' ]
		elif ch == '\\':
			self.nextToken = self.TOKEN[ 'BACKSLASH' ]
		else:
			self.nextToken = self.CHAR_CLASSES[ 'EOF' ]
		self.getChar()
		return self.nextToken

	def getNonBlank( self ):
		"""
		Call getChar until whitespace no longer encountered
		"""
		while self.nextChar.isspace():
			self.getChar() 

	def lex( self ):
		"""
		Main lexical function, returns nextToken
		"""
		self.lexeme = []
		self.lexeme2 = []
		self.getNonBlank()
		# case IDENT/RESERVED_WORD
		if self.charClass == self.CHAR_CLASSES[ 'LETTER' ]:
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != self.CHAR_CLASSES[ 'LETTER' ] and self.charClass != self.CHAR_CLASSES[ 'DIGIT' ] ):
					break
			if ''.join( self.lexeme ) not in self.RESERVED_WORDS:
				self.nextToken = self.TOKEN[ 'IDENT' ]
				self.lexeme = "ID"
			else:
				# find the "token value" corresponding to the reserved word found
				value = self.RESERVED_WORDS[ ''.join( self.lexeme ) ]
				self.nextToken = self.TOKEN[ value ]
		# case FLOATCONST/INTCONST
		elif self.charClass == self.CHAR_CLASSES[ 'DIGIT' ]:
			dotFlag = 0
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != self.CHAR_CLASSES[ 'DIGIT' ] ):
					if dotFlag == 1:
						break
					elif self.charClass == self.CHAR_CLASSES[ 'DOT' ]:
						self.addChar()
						self.getChar()
						dotFlag = 1
					else:
						self.error( self.charClass, self.CHAR_CLASSES[ 'DOT' ] )
			if dotFlag == 1:
				self.nextToken = self.TOKEN[ 'FLOAT_LIT' ]
				self.lexeme = "FLOATCONST"
			else:
				self.nextToken = self.TOKEN[ 'INT_LIT' ]
				self.lexeme = "NUMCONST"
		# cases + or -, check if unary operator or just operator
		elif self.charClass == self.CHAR_CLASSES[ 'ADD' ]:
			self.addChar()
			self.getChar()
			if( self.charClass != self.CHAR_CLASSES[ 'ADD' ] ):
				self.nextToken = self.TOKEN[ 'ADD_OP' ]
			else:
				self.nextToken = self.TOKEN[ 'UNARY_ADD_OP' ]
		elif self.charClass == self.CHAR_CLASSES[ 'SUB' ]:
			self.addChar()
			self.getChar()
			if( self.charClass != self.CHAR_CLASSES[ 'SUB' ] ):
				self.nextToken = self.TOKEN[ 'SUB_OP' ]
			else:
				self.nextToken = self.TOKEN[ 'UNARY_SUB_OP' ]
		# case CHARCONST
		elif self.charClass == self.CHAR_CLASSES[ 'SINGLE_QUOTE' ]:
			self.addChar()
			self.getChar()
			if self.charClass == self.CHAR_CLASSES[ 'LETTER' ]:
				self.addChar()
				self.getChar()
				if self.charClass == self.CHAR_CLASSES[ 'SINGLE_QUOTE' ]:
					self.nextToken = self.TOKEN[ 'CHAR_LIT' ]
					self.lexeme = "CHARCONST"
				else:
					self.error( self.charClass, self.CHAR_CLASSES[ 'SINGLE_QUOTE' ] )
			else:
				self.error( self.charClass, self.CHAR_CLASSES[ 'LETTER' ] )
		# case unknown, go to lookup
		elif self.charClass == self.CHAR_CLASSES[ 'UNKNOWN' ]:
			self.lookup( self.nextChar )
		elif self.charClass == self.CHAR_CLASSES[ 'EOF' ]:
			self.nextToken = self.CHAR_CLASSES[ 'EOF' ]
			self.lexeme = "EOF"
		return ( self.nextToken, ''.join( self.lexeme ), ''.join( self.lexeme2 ) )