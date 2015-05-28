class dictionaries:
	def __init__( self ):
		# reserved words
		self.RESERVED_WORDS = {	'int' : 'TYPE',
								'char' : 'TYPE',
								'float' : 'TYPE',
								'bool' : 'TYPE',
								'if' : 'CONDITIONAL' }

		# token codes
		self.TOKEN = {	'INT_LIT' : 10,
						'IDENT' : 11,
						'TYPE' : 12,
						'ASSIGN_OP' : 20,
						'ADD_OP' : 21,
						'SUB_OP' : 22,
						'MULT_OP' : 23,
						'DIV_OP' : 24,
						'LEFT_PAREN' : 25,
						'RIGHT_PAREN' : 26,
						'SEMICOLON' : 30 }

	def getReservedWordsDict( self ):
		return self.RESERVED_WORDS

	def getTokenDict( self ):
		return self.TOKEN