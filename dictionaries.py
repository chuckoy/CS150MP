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
								'while' : 'LOOP',
								'in' : 'IN',
								'return' : 'RETURN',
								'or' : 'LOGIC',
								'and' : 'LOGIC',
								'not' : 'LOGIC',
								'true' : 'TRUTH',
								'false' : 'TRUTH',
								'print' : 'IO',
								'scan' : 'IO',
								'break' : 'BREAK',
								'main' : 'MAIN',
								}

		# token codes
		self.TOKEN = {	'INT_LIT' : 10,
						'IDENT' : 11,
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
						'EQUAL_REL_OP' : 40,
						'LESS_REL_OP' : 41,
						'GREATER_REL_OP' : 42,
						'LESS_EQUAL_REL_OP' : 43,
						'GREATER_EQUAL_REL_OP' : 44,
						'NOT_EQUAL_REL_OP' : 45,
						'ADD_ASSIGN_OP' : 46,
						'SUB_ASSIGN_OP' : 47,
						'DOT' : 80,
						'BACKSLASH' : 81,
						'TYPE' : 600,
						'CONDITIONAL' : 601,
						'LOOP' : 602,
						'IN' : 603,
						'RETURN' : 604,
						'LOGIC' : 605,
						'TRUTH' : 606,
						'IO' : 607,
						'BREAK' : 608,
						'MAIN' : 999
						 }

	def getReservedWordsDict( self ):
		return self.RESERVED_WORDS

	def getTokenDict( self ):
		return self.TOKEN
