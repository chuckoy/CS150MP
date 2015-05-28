import sys
from data_handler import *

class SemanticAnalyzer:
    def __init__(self,content=None,reserve=None,types=None):
        self.content = content
        self.reserve = reserve
        self.types = types
        self.data = Data()

    #def type_checking(self,exp):


    def setContent(self,content):
        self.content = content

    """
        Handles variable declaration.
        t -> type of variable being declared.
        var -> name of variable
    """
    def declare_variable(self,exp):
        t = exp[0][0]
        var = exp[1][0]
        if exp[2][1] == 'SEMICOLON':
            self.data.addData([var,t,None])
        elif exp[2][1] == 'ASSIGN_OP':
            if exp[3][1] == 'CONSTNUM':
                val = int(exp[3][0])
            if self.data.checkDataType(val) == t:
                self.data.addData([var,t,val])
            else:
                print "Type mismatch."

    
    #def identifier_operations(self,exp):
        #exp_copy = [exp[x][0] in xrange(len(exp))]
        #if 

    """
        Analyzes each line of code.
    """
    def analyze_block(self):
        for block in self.content:
            path = block[0][1]
            if path == 'TYPE':
                self.declare_variable(block)
            elif path == 'IDENTIFIER':
                print "dunno"
        print self.data.data

#content[block][elements_of_block]
content = [
    [
        ['int','TYPE'],
        ['a','IDENT'],
        ['=','ASSIGN_OP'],
        ['3','CONSTNUM'],
        [';','SEMICOLON']
    ],
    [
        ['int','TYPE'],
        ['b','IDENTIFIER'],
        ['=','ASSIGN_OP'],
        ['4','CONSTNUM'],
        [';','SEMICOLON']
    ],
    [
        ['a','IDENTIFIER'],
        ['+','ADD_OP'],
        ['b','IDENTIFIER'],
        [';','SEMICOLON']
    ]
]

d = dictionaries()
s = SemanticAnalyzer(content=content,types=d.DTYPES)

s.analyze_block()