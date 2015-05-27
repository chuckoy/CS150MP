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
							'UNKNOWN' : 99 }
		self.RESERVED_WORDS = dicts.getReservedWordsDict()
		self.TOKEN = dicts.getTokenDict()

	def run( self ):
		"""
		Returns a list of the tokens from the given inFileName in the constructor
		"""
		tokens = []
		with open( self.inFileName, 'r' ) as self.in_fp:
			while self.charClass != self.CHAR_CLASSES[ 'EOF' ]:
				tokens.append( self.lex() )
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
			self.self.nextToken = self.TOKEN[ 'LEFT_PAREN' ]
		elif ch == ')':
			self.nextToken = self.TOKEN[ 'RIGHT_PAREN' ]
		elif ch == '+':
			self.nextToken = self.TOKEN[ 'ADD_OP' ]
		elif ch == '-':
			self.nextToken = self.TOKEN[ 'SUB_OP' ]
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
		if self.charClass == self.CHAR_CLASSES[ 'LETTER' ]:
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != self.CHAR_CLASSES[ 'LETTER' ] and self.charClass != self.CHAR_CLASSES[ 'DIGIT' ] ):
					break
			self.nextToken = self.TOKEN[ 'IDENT' ]
		elif self.charClass == self.CHAR_CLASSES[ 'DIGIT' ]:
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != self.CHAR_CLASSES[ 'DIGIT' ] ):
					break
			self.nextToken = self.TOKEN[ 'INT_LIT' ]
		elif self.charClass == self.CHAR_CLASSES[ 'UNKNOWN' ]:
			self.lookup( self.nextChar )
			self.getChar()
		elif self.charClass == self.CHAR_CLASSES[ 'EOF' ]:
			self.nextToken = self.CHAR_CLASSES[ 'EOF' ]
			self.lexeme = "EOF"
		#print( 'Next token is: ', self.nextToken, ', next lexeme is ', ''.join( self.lexeme ) )
		return self.nextToken