class ReservedWords:
	def __init__( self ):
		RESERVED_WORDS = {	'int' : 'type',
							'char' : 'type',
							'float' : 'type',
							'bool' : 'type',
							'if' : 'conditional' }

	def getReservedWords( self ):
		return RESERVED_WORDS