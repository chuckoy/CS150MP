class RecursiveDescent:
	def __init__(self):
		self.in_fp = []
		self.i = 0
		self.lexeme = []
		self.token = 0
		self.charClass = 0
		self.nextToken = 0
		self.noParen = 0

		# character classes
		CHAR_CLASSES = {	'EOF' : -1,	
							'LETTER' : 0,
							'DIGIT' : 1,
							'UNKNOWN' : 99 }

		# token codes
		TOKEN = {	'INT_LIT' : 10,
					'IDENT' : 11,
					'TYPE' : 12,
					'ASSIGN_OP' : 20,
					'ADD_OP' : 21,
					'SUB_OP' : 22,
					'MULT_OP' : 23,
					'DIV_OP' : 24,
					'LEFT_PAREN' : 25,
					'RIGHT_PAREN' : 26 }

		RESERVED_WORDS = {	'int' : 'placeholder',
							'char' : 'placeholder',
							'float' : 'placeholder',
							'bool' : 'placeholder' }

	def getChar( self ):
		if self.i < len( self.in_fp ):
			self.nextChar = self.in_fp[ self.i ]
			self.i += 1
			if( self.nextChar.isalpha() ) self.charClass = CHAR_CLASSES[ LETTER ]
			elif( self.nextChar.isdigit() ) self.charClass = CHAR_CLASSES[ DIGIT ]
			else self.charClass = CHAR_CLASSES[ UNKNOWN ]
		else:
			self.charClass = CHAR_CLASSES[ EOF ]

	def addChar( self ):
		self.lexeme.append( chr( nextChar ) )

	def lookup( self, ch ):
		self.addChar()
		if ch == '(':
			self.nextToken = TOKEN[ LEFT_PAREN ]
		elif ch == ')':
			self.nextToken = TOKEN[ RIGHT_PAREN ]
		elif ch == '+':
			self.nextToken = TOKEN[ ADD_OP ]
		elif ch == '-':
			self.nextToken = TOKEN[ SUB_OP ]
		elif ch == '*':
			self.nextToken = TOKEN[ MULT_OP ]
		elif ch == '/':
			self.nextToken = TOKEN[ DIV_OP ]
		elif ch == '=':
			self.nextToken = TOKEN[ ASSIGN_OP ]
		else:
			self.nextToken = CHAR_CLASSES[ EOF ]
		return self.nextToken

	def getNonBlank( self ):
		while self.nextChar.isspace():
			self.getChar() 

	def lex( self ):
		self.lexeme = []
		self.getNonBlank()
		if self.charClass == CHAR_CLASSES[ LETTER ]:
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != CHAR_CLASSES[ LETTER ] && self.charClass != CHAR_CLASSES[ DIGIT ] ):
					break
			self.nextToken = TOKEN[ IDENT ]
		elif self.charClass == CHAR_CLASSES[ DIGIT ]:
			while True:
				self.addChar()
				self.getChar()
				if( self.charClass != CHAR_CLASSES[ DIGIT ] ):
					break
			self.nextToken = TOKEN[ INT_LIT ]
		elif self.charClass == CHAR_CLASSES[ UNKNOWN ]:
			self.lookup( self.nextChar )
			self.getChar()
		elif self.charClass == CHAR_CLASSES[ EOF ]:
			self.nextToken = CHAR_CLASSES[ EOF ]
			lexeme = "EOF"
		print( 'Next token is: ', self.nextToken, ', next lexeme is ', self.lexeme )
		return nextToken

	def start( self ):
		print( 'Enter start()' )
		if self.nextToken == TOKEN[ TYPE ]:
			self.lex()

	def error(self):
		tokens=[ '+', '-', '/', '*', 'a', 'b', 'c', '(', ')', '=' ]
		# error caused by lexeme read at a rule
		if tokens.count( "".join( self.lexer.lexeme ) ) > 0:
			print "Syntax Error"
		else:
			print "Lexical Error in input. Lexeme","".join(self.lexer.lexeme),"is not in the grammar. Input is not generated by the grammar."

	def iden(self):# A->id=E
		print "Enter <A>"
		if self.lexer.nextToken==self.lexer.IDENT or self.lexer.nextToken==self.lexer.INT_LIT:
			self.id()#parse the id
			if self.lexer.nextToken==self.lexer.ASSIGN_OP:#see if ang susunod ay =
				self.lexer.lex()
				self.expr()#parse expresison
			else:
				self.error()#not = after id
		else:
			self.error()
		if self.lexer.noParen!=0:#same no. of ( and ) in the input
			self.error()
		print "Exit <A>"
	def expr(self):#E->TE'
		print "Enter <E>"
		self.term()#parse the first term
		self.exprP()
		print "Exit <E>"
	def exprP(self):# E'->{(+|-)TE'}
		print "Enter <E'>"
		while self.lexer.nextToken==self.lexer.ADD_OP or self.lexer.nextToken==self.lexer.SUB_OP:#as long as + or - comes next
			self.lexer.lex()
			self.term()
		print "Exit <E'>"
	def term(self):# T->FT'
		print "Enter <T>"
		self.factor()#parse the first factor
		self.termP()
		print "Exit <T>"
	def termP(self):# T'->{(*|\)FT'}
		print "Enter <T'>"
		while self.lexer.nextToken==self.lexer.MULT_OP or self.lexer.nextToken==self.lexer.DIV_OP:#as long as * or / comes next
			self.lexer.lex()
			self.factor()
		print "Exit <T'>"
	def factor(self):# F->(E)|id
		print "Enter <F>"
		#self.lexer.lex()
		if self.lexer.nextToken==self.lexer.IDENT or self.lexer.nextToken==self.lexer.INT_LIT:
			#self.lexer.lex()#get token 
			self.id()

		else: #(<expr>)
			if self.lexer.nextToken==self.lexer.LEFT_PAREN:
				self.lexer.lex()
				self.expr()
				if self.lexer.nextToken==self.lexer.RIGHT_PAREN:
					self.lexer.lex()
				else:
					self.error()
			else: #It was not an id, an integer literal, or a left parenthesis
				self.error()
		print "Exit <F>"
	def id(self):# id->(a|b|c)
		print "Enter <id>"
		self.lexer.lex()
		print "Exit <id>"
		
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