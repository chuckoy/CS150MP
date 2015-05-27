class RecursiveDescent:
	def __init__( self, resWords ):
		in_fp = []
		self.i = 0
		lexeme = []
		self.token = 0
		charClass = 0
		nextToken = 0
		self.noParen = 0

		'''
			ERROR CODES:
			100	:	Reserved word conflict
		'''

		# character classes
		CHAR_CLASSES = {	'EOF' : -1,	
							'LETTER' : 0,
							'DIGIT' : 1,
							'UNKNOWN' : 99 }

		# token codes
		TOKEN = {	'INT_LIT' : 10,
					'IDENT' : 11,
					'ASSIGN_OP' : 20,
					'ADD_OP' : 21,
					'SUB_OP' : 22,
					'MULT_OP' : 23,
					'DIV_OP' : 24,
					'LEFT_PAREN' : 25,
					'RIGHT_PAREN' : 26,
					'SEMICOLON' : 30 }

		RESERVED_WORDS = resWords

	def getChar( self ):
		if self.i < len( in_fp ):
			self.nextChar = in_fp[ self.i ]
			self.i += 1
			if( self.nextChar.isalpha() ) charClass = CHAR_CLASSES[ LETTER ]
			elif( self.nextChar.isdigit() ) charClass = CHAR_CLASSES[ DIGIT ]
			else charClass = CHAR_CLASSES[ UNKNOWN ]
		else:
			charClass = CHAR_CLASSES[ EOF ]

	def addChar( self ):
		lexeme.append( chr( nextChar ) )

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
		while self.nextChar.isspace():
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
			self.lookup( self.nextChar )
			self.getChar()
		elif charClass == CHAR_CLASSES[ EOF ]:
			nextToken = CHAR_CLASSES[ EOF ]
			lexeme = "EOF"
		print( 'Next token is: ', nextToken, ', next lexeme is ', lexeme )
		return nextToken

	def start( self ):
		print "Enter start()"
		self.declaration()
		print "Exit start()"

	def declaration( self ):
		print "Enter declaration()"
		if nextToken == TOKEN[ IDENT ]:
			self.type()
			self.var()
			if nextToken == TOKEN[ ASSIGN_OP ]:
				self.lex()
				self.expr()
			else:
				self.error()
		print "Exit declaration()"

	def expr( self ):#E->TE'
		print "Enter expr()"
		self.term()#parse the first term
		self.exprP()
		print "Exit expr()"
	def exprP( self ):# E'->{(+|-)TE'}
		print "Enter exprP()"
		if nextToken != CHAR_CLASSES[ EOF ]:
			if nextToken == TOKEN[ ADD_OP ] or nextToken == TOKEN[ SUB_OP ]:
				self.lex()
				self.term()
				self.exprP()
		print "Exit exprP()"
	def term( self ):# T->FT'
		print "Enter term()"
		self.factor()#parse the first factor
		self.termP()
		print "Exit term()"
	def termP( self ):# T'->{(*|\)FT'}
		print "Enter termP()"
		while self.nextToken==self.MULT_OP or self.nextToken==self.DIV_OP:#as long as * or / comes next
			self.lex()
			self.factor()
		print "Exit termP()"
	def factor( self ):# F->(E)|id
		print "Enter factor()"
		#self.lex()
		if self.nextToken==self.IDENT or self.nextToken==self.INT_LIT:
			#self.lex()#get token 
			self.id()

		else: #(<expr>)
			if self.nextToken==self.LEFT_PAREN:
				self.lex()
				self.expr()
				if self.nextToken==self.RIGHT_PAREN:
					self.lex()
				else:
					self.error()
			else: #It was not an id, an integer literal, or a left parenthesis
				self.error()
		print "Exit factor()"

	def id( self ):# id->(a|b|c)
		print "Enter <id>"
		self.lex()
		if lexeme in RESERVED_WORDS:
			self.error( 100 )
		print "Exit <id>"

	def error( self, errorCode = 0 ):
		if errorCode == 0:
			tokens=['+','-','/','*','a','b','c','(',')','=']
			if tokens.count("".join(self.lexeme))>0:#error caused by lexeme read at a rule
				print "Syntax Error"
			else:
				print "Lexical Error in input. Lexeme","".join(self.lexeme),"is not in the grammar. Input is not generated by the grammar."
		elif errorCode == 100:
			print "Identifier expected. Reserved word gotten."
		
def main():
	# lexer=lexicalAnalyzer()
	# lexer.in_fp="(a+b)/c"
	# lexer.getChar()
	# lexer.lex()
	rec=recursiveDescent(lexicalAnalyzer())
	#rec.lexer.in_fp="b=a+c"
	rec.lexer.in_fp=raw_input("Enter your input: ")
	rec.lexer.getChar()
	rec.lexer.lex()
	rec.iden()
	# while lexer.nextToken!=-1:
	# 	lexer.lex()

		

		
if __name__ == '__main__':
	main()