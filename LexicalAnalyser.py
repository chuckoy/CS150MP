class LexicalAnalyser:
	"""
		:param inFileName:  name of input file
		:param resWords: reservedWords class instance
	""" 
	def __init__( self, inFileName, dicts ):
		self.inFileName = inFileName

		lexeme = []
		charClass = 0
		nextChar = ""

		# character classes
		CHAR_CLASSES = {	'EOF' : -1,	
							'LETTER' : 0,
							'DIGIT' : 1,
							'UNKNOWN' : 99 }
		RESERVED_WORDS = dicts.getReservedWordsDict()
		TOKENS = dicts.getTokenDict()

	def run( self ):
		tokens = []
		with open( self.inFileName, 'r' ) as in_fp:
			while charClass != CHAR_CLASSES[ EOF ]:
				tokens.append( self.lex() )
				print tokens
		return tokens

	def getChar( self ):
		nextChar = in_fp.read( 1 )
		if charClass != CHAR_CLASSES[ EOF ]:
			if nextChar.isalpha():
				charClass = CHAR_CLASSES[ LETTER ]
			elif nextChar.isdigit():
				charClass = CHAR_CLASSES[ DIGIT ]
			else:
				charClass = CHAR_CLASSES[ UNKNOWN ]
		else:
			charClass = CHAR_CLASSES[ EOF ]

	def addChar( self ):
		lexeme.append( chr( nextChar ) )

	"""
		:param ch: the char that is being looked up
	"""
	def lookup( self, ch ):
		self.addChar()
		if ch == '(':
			nextToken = TOKEN[ LEFT_PAREN ]
		elif ch == ')':
			nextToken = TOKEN[ RIGHT_PAREN ]
		elif ch == '+':
			nextToken = TOKEN[ ADD_OP ]
		elif ch == '-':
			nextToken = TOKEN[ SUB_OP ]
		elif ch == '*':
			nextToken = TOKEN[ MULT_OP ]
		elif ch == '/':
			nextToken = TOKEN[ DIV_OP ]
		elif ch == '=':
			nextToken = TOKEN[ ASSIGN_OP ]
		elif ch == ';':
			nextToken = TOKEN[ SEMICOLON ]
		else:
			nextToken = CHAR_CLASSES[ EOF ]
		return nextToken

	def getNonBlank( self ):
		while nextChar.isspace():
			self.getChar() 

	def lex( self ):
		lexeme = []
		self.getNonBlank()
		if charClass == CHAR_CLASSES[ LETTER ]:
			while True:
				self.addChar()
				self.getChar()
				if( charClass != CHAR_CLASSES[ LETTER ] && charClass != CHAR_CLASSES[ DIGIT ] ):
					break
			nextToken = TOKEN[ IDENT ]
		elif charClass == CHAR_CLASSES[ DIGIT ]:
			while True:
				self.addChar()
				self.getChar()
				if( charClass != CHAR_CLASSES[ DIGIT ] ):
					break
			nextToken = TOKEN[ INT_LIT ]
		elif charClass == CHAR_CLASSES[ UNKNOWN ]:
			self.lookup( nextChar )
			self.getChar()
		elif charClass == CHAR_CLASSES[ EOF ]:
			nextToken = CHAR_CLASSES[ EOF ]
			lexeme = "EOF"
		print( 'Next token is: ', nextToken, ', next lexeme is ', lexeme )
		return nextToken