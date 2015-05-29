import sys
from data_handler import *
from utils import *

class SemanticAnalyzer:
    def __init__(self,content=None,reserve=None,types=None):
        self.content = content
        self.reserve = reserve
        self.types = types
        self.process = Process()
        self.data = Data()
        self.continue_flag = 1

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
                self.continue_flag = 0

    def operation_type_checking_and_computation(self,exp):
        tags = [exp[x][1] for x in xrange(len(exp))]
        exp = [exp[x][0] for x in xrange(len(exp))]
        tree = postToTree(*infixToPostfix(exp,tags))
        pref,pref_tags = prefixFromTree(tree)

        pref = pref[::-1]
        pref_tags = pref_tags[::-1]

        stack = []
        stack_tags = []
        er = False
        for i in xrange(len(pref)):
            if pref[i] not in OPERATOR:

                if pref_tags[i] == 'IDENT':
                    val = self.data.data[pref[i]][1]
                    val_tag = self.data.data[pref[i]][0]
                else:
                    val = pref[i]
                    val_tag = pref_tags[i]

                stack.append(val)
                stack_tags.append(val_tag)
            else:
                op1 = stack.pop()
                op2 = stack.pop()

                op1_tag = stack_tags.pop()
                op2_tag = stack_tags.pop()
                res = self.process.perform(pref[i],[op1,op2])

                #IF THERE IS NO ERROR IN COMPUTATION
                if res != None:
                    stack.append(res)
                    stack_tags.append(op1_tag)
                else:
                    er = 1
                    break
        if not er:
            return stack.pop(),stack_tags.pop()
        else:
            return


    def operations(self,exp):
        exp_copy = [exp[x][0] in xrange(len(exp))]
        if '=' == exp[1][0]:
            var = exp[0][0]


    """
        Analyzes each line of code.
    """
    def analyze_block(self):
        for block in self.content:
            path = block[0][1]
            if path == 'TYPE':
                self.declare_variable(block)
                if self.continue_flag ==0:
                    break
            elif path == 'IDENT':
                print self.operation_type_checking_and_computation(block)
        #print self.data.data

#content[block][elements_of_block]

content = [
    [
        ['int','TYPE'],
        ['a','IDENT'],
        ['=','ASSIGN_OP'],
        ['3','CONSTNUM']
        #[';','SEMICOLON']
    ],
    [
        ['int','TYPE'],
        ['b','IDENT'],
        ['=','ASSIGN_OP'],
        ['4','CONSTNUM']
        #[';','SEMICOLON']
    ],
    [
        ['a','IDENT'],
        ['+','ADD_OP'],
        ['b','IDENT']
        #[';','SEMICOLON']
    ]
]


d = dictionaries()
s = SemanticAnalyzer(content=content,types=d.DTYPES)

s.analyze_block()