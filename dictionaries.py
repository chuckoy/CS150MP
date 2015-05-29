class dictionaries:
	def __init__( self ):
		# reserved words
		self.RESERVED_WORDS = {	'int' : 'TYPE',
								'char' : 'TYPE',
								'float' : 'TYPE',
								'bool' : 'TYPE',
								'if' : 'CONDITIONAL',
								'else' : 'CONDITIONAL',
								'foreach' : 'LOOP',
								'for' : 'LOOP',
								'while' : 'LOOP'
								'in' : 'IN',
								'return' : 'RETURN',
								'or' : 'LOGIC',
								'and' : 'LOGIC',
								'not' : 'LOGIC',
								'true' : 'TRUTH',
								'false' : 'TRUTH',
								'print' : 'IO',
								'scan' : 'IO',
								'break' : 'BREAK' }

		# token codes
		self.TOKEN = {	'INT_LIT' : 10,
						'IDENT' : 11,
						'TYPE' : 12,
						'FLOAT_LIT' : 13,
						'CHAR_LIT' : 14,
						'ASSIGN_OP' : 20,
						'ADD_OP' : 21,
						'SUB_OP' : 22,
						'MULT_OP' : 23,
						'DIV_OP' : 24,
						'LEFT_PAREN' : 25,
						'RIGHT_PAREN' : 26,
						'UNARY_ADD_OP' : 27,
						'UNARY_SUB_OP' : 28,
						'SEMICOLON' : 30,
						'LEFT_CURLY' : 31,
						'RIGHT_CURLY' : 32,
						'DOT' : 80,
						'BACKSLASH' : 81 }

		#data types
		self.DTYPES = ['int','char','float','bool']

	def getReservedWordsDict( self ):
		return self.RESERVED_WORDS

	def getTokenDict( self ):
		return self.TOKEN
