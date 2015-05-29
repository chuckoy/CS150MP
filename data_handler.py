from dictionaries import *

class Tree:
    def __init__(self,data=None,children=[],parent=None):
        self.data = data
        self.parent = parent
        self.children = children

    def setData(self,data):
        self.data = data

    def addChild(self,child):
        if child in self.children:
            pass
        else:
            self.children.append(child)

    def setParent(self,parent):
        self.parent = parent

class BinTree(Tree):
    def __init__(self,data=None,rChild=None,lChild=None,parent=None,canHaveChild=1):
        self.data = data
        self.rChild = rChild
        self.lChild = lChild
        self.parent = parent
        self.canHaveChild = canHaveChild

    def addChild(self,child,lr):
        if lr == 'l':
            self.lChild = child
        else:
            self.rChild = child

class Process:
    def __init__(self):
        return

    def compare(self,id_,args):
        if id_ == '==':
            if args[0] == args[1]:
                return True
            return False
        elif id_ == '>':
            if args[0] > args[1]:
                return True
            return False
        elif id_ == '<':
            if args[0] < args[1]:
                return True
            return False
        elif id_ == '>=':
            if args[0] >= args[1]:
                return True
            return False
        elif id_ == '<=':
            if args[0] <= args[1]:
                return True
            return False

    def perform(self,id_,args):
        if id_ == '+':
            return self.add(args)
        elif id_ == '-':
            return self.sub(*args)
        elif id_ == '*':
            return self.multiply(*args)
        elif id_ == '/':
            return self.divide(*args)

    def add(self,*args):
        try:
            return sum(*args)
        except:
            print "Error here. Cannot add non numerical data."
    
    def sub(self,num1,num2):
        try:
            return num1-num2
        except:
            print "Error here. Cannot subtract non numerical data."

    def multiply(self,num1,num2):
        if isinstance(num1, (int,float)) and isinstance(num2, (int,float)):
            return num1*num2
        else:
            print "Type error. Cannot multiply non numerical data."

    def divide(self,num1,num2):
        try:
            return num1/num2
        except:
            print "Division error. Cannot divide by zero."


    #def sub(self,*args):

"""
Contains variables of the program as well as the corresponding data type and value
"""
class Data:
    def __init__(self,data={}):
        self.data = data

    """
        Add new variable to the pool of variables.
        info[0] -> name of variable
        info[1] -> data type of variable
        info[2] -> value of variable
    """
    def addData(self,info):
        self.data[info[0]] = [info[1],info[2]]

    """
        Returns the data type of value.
    """
    def checkDataType(self,value):
        if type(value) == int:
            return 'int'
        elif type(value) == float:
            return 'float'
        elif type(value) == bool:
            return 'bool'
        elif type(value) == str:
            return 'char'
        else:
            return "Syntax error."

    """
        Modify the value of an existing variable if it exists,
        return an error if variable does not exist or if the 
        variable and the new value don't match types
    """
    def modifyData(self,var,newValue):
        try:
            if self.checkDataType(newValue) == self.data[var][0]:
                self.data[var][1] = newValue
            else:
                print "Type mismatch."
        except:
            print "Variable %s has not been declared." % var