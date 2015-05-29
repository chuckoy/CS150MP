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
        l = len(exp)
        if l > 2:
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
        else:
            if exp[0][0] == 'int':
                self.data.addData([var,t,0])
        

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
                    try:
                        val = self.data.data[pref[i]][1]
                        val_tag = self.data.data[pref[i]][0]
                    except:
                        print "Key value error"
                        er = 1
                        break
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

    def find_semi_colon(self,block):
        ind = []
        for x in xrange(len(block)):
            if block[x] == ';':
                ind.append(x)
        return ind

    def copy_lexeme(self,block):
        return [block[x][0] for x in xrange(len(block))]

    def copy_token(self,block):
        return [block[x][1] for x in xrange(len(block))]

    def strip_semicolon(self,block):
        copy_lexeme = self.copy_lexeme(block)
        copy_token =  self.copy_token(block)
        ind = self.find_semi_colon(copy_lexeme)
        for x in xrange(len(ind)):
            copy_lexeme.pop(ind[x])
            copy_token.pop(ind[x])
            for x in xrange( len(ind)):
                ind[ x ] -= 1
        ret_value = []
        for x in xrange(len(copy_lexeme)):
            ret_value.append( [copy_lexeme[x],copy_token[x]] )
        return ret_value

    """
        Analyzes each line of code.
    """
    def analyze_block(self):
        for block in self.content:
            path = block[0][1]
            if path == 'TYPE':
                block_copy = self.strip_semicolon(block)
                self.declare_variable(block_copy)
                if self.continue_flag ==0:
                    break
            elif path == 'IDENT':
                block_copy = self.strip_semicolon(block)
                print self.operation_type_checking_and_computation(block_copy)
        self.print_data()
    def print_data(self):
        for key in self.data.data.keys():
            print "Varname: ", key, " datatype, value: ", self.data.data[key]
    """
    def analyze_elems(self,cblock):
        path = block[0][1]
        if path == 'TYPE':
            self.declare_variable(block)
            if self.continue_flag ==0:
                break
        elif path == 'IDENT':
            print self.operation_type_checking_and_computation(block)   
    """
        #print self.data.data
    def find_condition(self,block):
        leftParen = -1
        rightParen = -1
        for x in xrange(len(block)):
            if block[x][1] == 'LEFT_PAREN':
                leftParen = x
                break

        for x in xrange(len(block)):
            if block[x][1] == 'RIGHT_PAREN':
                rightParen = x
                break
        return leftParen,rightParen

    def get_groups(self,block):
        ind = 0
        groups = []
        for x in xrange(len(block)):
            if block[x][0] == '(' or block[x][0] == '{' or block[x][0] == '[':
                ind = x
                ind_end = x
                for trav in xrange(x,len(block)):
                    if block[trav][0] == ')' or block[trav][0] == '}' or block[trav][0] == ']':
                        ind_end = trav
                        break
                groups.append([ind,ind_end+1])
                #groups.append(block[ind,ind_end+1])
        return groups

    def get_per_lines(self,group):
        group.pop(0)
        group.pop(len(group)-1)

        lines = []
        pointer = 0
        for x in xrange(len(group)):
            if group[pointer][0] == '{' or group[pointer][0] == '(':
                pointer += 1
            if group[x][0] == ';':
                lines.append([pointer,x])
                pointer = x + 1
        return lines

    def get_next_line(self,block,curPoint):
        curPoint += 1
        line = []

        for x in xrange(curPoint,len(block)):
            if block[x][0] != ';':
                line.append( block[x] )
            elif block[x][0] == ';':
                curPoint = x
                break
        return line,curPoint


    def check_condition(self,block,leftParen,rightParen):
        """
        Analyzes condition. Current conditions handled are equality/inequality
        conditions. Also handles TRUE and FALSE conditions.

        :param block: expression.
        :param leftParen: index of left parenthesis.
        :param rightParen: index of right parenthesis.

        returns True or False

        """
        if block[leftParen+1][0] == 'TRUE' or block[leftParen+1][0] == 'FALSE':
            if block[leftParen+1][0] == 'TRUE':
                return True
            else:
                return False
        else:
            var_value = self.data.data[block[leftParen+1]][1]
            cond = block[leftParen+2]
            comp = block[leftParen+3]
            return self.process.compare(cond,[var_value,comp])