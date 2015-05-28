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
			else:
				self.charClass = self.CHAR_CLASSES[ 'UNKNOWN' ]
		else:
			self.charClass = self.CHAR_CLASSES[ 'EOF' ]

	def addChar( self ):
		"""
		Append the character to the current lexeme (for tracking)
		"""
		self.lexeme.append( self.nextChar )

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
		self.getNonBlank()
		# case ident
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
		# case numConst
		elif self.charClass == self.CHAR_CLASSES[ 'DIGIT' ]:
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != self.CHAR_CLASSES[ 'DIGIT' ] ):
					break
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
		# case unknown, go to lookup
		elif self.charClass == self.CHAR_CLASSES[ 'UNKNOWN' ]:
			self.lookup( self.nextChar )
		elif self.charClass == self.CHAR_CLASSES[ 'EOF' ]:
			self.nextToken = self.CHAR_CLASSES[ 'EOF' ]
			self.lexeme = "EOF"
		return ( self.nextToken, ''.join( self.lexeme ) )