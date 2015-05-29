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
                elif exp[ 3 ][ 1 ] == 'CONSTFLOAT':
                    val = float( exp[ 3 ][ 0 ] )
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
                if op2_tag == "CONSTNUM":
                    op2 = int( op2 )
                if op2_tag == "CONSTFLOAT":
                    op2 = float( op2 )
                if op1_tag == "CONSTNUM":
                    op1 = int( op1 )
                if op1_tag == "CONSTFLOAT":
                    op1 = float( op1 )
                res = self.process.perform(pref[i],[op1,op2])

                #IF THERE IS NO ERROR IN COMPUTATION
                if res != None:
                    stack.append(res)
                    stack_tags.append(op1_tag)
                else:
                    er = 1
                    break
        if not er:
            return stack.pop()
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
        index = 0
        skip = 0
        for block in self.content:
            if skip == 0:
                index += 1
                path = block[0][1]
                if path == 'TYPE':
                    block_copy = self.strip_semicolon(block)
                    self.declare_variable(block_copy)
                    if self.continue_flag ==0:
                        break
                elif path == 'IDENT':
                    if block[1][1] == 'ASSIGN_OP':
                        copy_lexeme = self.copy_lexeme(block)
                        copy_token = self.copy_token(block)
                        copy_lexeme = copy_lexeme[2::]
                        copy_token = copy_token[2::]
                        new_block = [[x,y] for x,y in zip(copy_lexeme,copy_token)]
                        new_block = self.strip_semicolon(new_block)
                        val = self.operation_type_checking_and_computation(new_block)
                        self.data.modifyData(block[0][0],val)
                    else:
                        block_copy = self.strip_semicolon(block)
                        self.operation_type_checking_and_computation(block_copy)
                elif path == 'CONDITIONAL' and block[ 0 ][ 0 ] == "if":
                    skip = self.if_handler( block, self.content, index )
            else:
                skip -= 1
        self.print_data()

    def analyze_line(self, block):
        path = block[0][1]
        if path == 'TYPE':
            block_copy = self.strip_semicolon(block)
            self.declare_variable(block_copy)
        elif path == 'IDENT':
            if block[1][1] == 'ASSIGN_OP':
                copy_lexeme = self.copy_lexeme(block)
                copy_token = self.copy_token(block)
                copy_lexeme = copy_lexeme[2::]
                copy_token = copy_token[2::]
                new_block = [[x,y] for x,y in zip(copy_lexeme,copy_token)]
                new_block = self.strip_semicolon(new_block)
                val = self.operation_type_checking_and_computation(new_block)
                self.data.modifyData(block[0][0],val)
            else:
                block_copy = self.strip_semicolon(block)
                self.operation_type_checking_and_computation(block_copy)
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
        cond = []
        for x in xrange(len(block)):
            if block[x][1] == 'RIGHT_PAREN':
                rightParen = x
                break
            if block[x][1] == 'LEFT_PAREN':
                leftParen = x
            elif leftParen != -1:
                cond.append([ block[x][0],block[x][1] ])
        if leftParen == -1:
            return "TRUE", "TRUE", "TRUE"
        return leftParen,rightParen,cond

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


    def check_condition(self,block):
        """
        Analyzes condition. Current conditions handled are equality/inequality
        conditions. Also handles TRUE and FALSE conditions.

        :param block: expression.
        :param leftParen: index of left parenthesis.
        :param rightParen: index of right parenthesis.

        returns True or False

        """
        if block == 'TRUE' or block == 'FALSE':
            if block == 'TRUE':
                return True
            else:
                return False
        else:
            print block, "ASJD"
            var_value = self.data.data[block[0][0]][1]
            cond = block[1][ 0]     
            comp = block[2][ 0 ]
            return self.process.compare(cond,[var_value,comp])
    
    def find_left_curly(self,block):
        ind = []
        for x in xrange(len(block)):
            if block[x][0] == '{':
                ind.append(x)
        return ind

    #def get_if_lines(self,block):

    
    def if_handler(self,block, total, blockInd):
        lp, rp, cond = self.find_condition( block )
        lineCounter = 0
        """
        # this is else
        if cond == "TRUE":
            ind = self.find_left_curly(block)

            copy_lexeme = self.copy_lexeme(block)
            copy_token = self.copy_token(block)

            copy_lexeme = copy_lexeme[ind[0]+1::]
            copy_token = copy_token[ind[0]+1::]
            new_block = [[x,y] for x,y in zip(copy_lexeme,copy_token)]

            rightCurlyTest = [ [ '}', 'RIGHT_CURLY' ] ]
            next_block = total[ blockInd ]
            while next_block != rightCurlyTest:
                self.analyze_line( next_block )
                print "YOLO"
                # move to the next block
                blockInd += 1
                next_block = total[ blockInd ]
                lineCounter += 1
        # this is not else
        else:
        """
        if self.check_condition(cond):
            ind = self.find_left_curly(block)

            copy_lexeme = self.copy_lexeme(block)
            copy_token = self.copy_token(block)

            copy_lexeme = copy_lexeme[ind[0]+1::]
            copy_token = copy_token[ind[0]+1::]
            new_block = [[x,y] for x,y in zip(copy_lexeme,copy_token)]

            rightCurlyTest = [ [ '}', 'RIGHT_CURLY' ] ]
            next_block = total[ blockInd - 1 ]
            senpaiFirstTimeKo = 1
            while next_block != rightCurlyTest:
                if senpaiFirstTimeKo == 1:
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    senpaiFirstTimeKo -= 1
                print next_block, "try"
                self.analyze_line( next_block )
                # move to the next block
                blockInd += 1
                next_block = total[ blockInd ]
                lineCounter += 1
        else:
            print "PUMAPASOK"
            ind = self.find_left_curly(block)

            copy_lexeme = self.copy_lexeme(block)
            copy_token = self.copy_token(block)

            copy_lexeme = copy_lexeme[ind[0]+1::]
            copy_token = copy_token[ind[0]+1::]
            new_block = [[x,y] for x,y in zip(copy_lexeme,copy_token)]

            rightCurlyTest = [ [ '}', 'RIGHT_CURLY' ] ]
            next_block = total[ blockInd ]
            while next_block != rightCurlyTest:
                # move to the next block
                blockInd += 1
                next_block = total[ blockInd ]
                lineCounter += 1
            blockInd += 1
            next_block = total[ blockInd ]
            lineCounter += 1
            elseEntered = 1
            while next_block != rightCurlyTest:
                if elseEntered == 1:
                    next_block.pop( 0 )
                    next_block.pop( 0 )
                    elseEntered -= 1
                self.analyze_line( next_block )
                print next_block
                # move to the next block
                blockInd += 1
                next_block = total[ blockInd ]
                lineCounter += 1
        return lineCounter
        #if( self.check_condition(block,lp,rp) ):
    