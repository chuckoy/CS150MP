from data_handler import BinTree

OPERATOR = ['+','-','*','/','%']
PREC = {
    '*':3,
    '/':3,
    '%':3,
    '+':2,
    '-':2,
}

ERRORS = {
    'keyvalue':"Key value error",

}

#FUNCTION NOT FUNCTIONAL
def postToTree(data,tags):
    """
        Tree constructed contains a lexeme and a token.
        To access lexeme access Tree.data[0], token is
        Tree.data[1]
        :param data: List of value to be stored in the nodes.
        :param tags: List of tags corresponding the given data.
        :return root: Returns the root node of the constructed tree.
    """
    data = data[::-1]
    tags = tags[::-1]

    root = BinTree(data=[data[0],tags[0]])
    curNode = root

    pointer = 1
    while pointer < len(data):
        node = BinTree(data=[data[pointer],tags[pointer]])
        d = data[pointer]
        t = tags[pointer]
        print d,t
        
        while True:
            if curNode.rChild == None and curNode.data[0] in OPERATOR:
                curNode.rChild = node
                node.setParent(curNode)
                curNode = node
                break
            elif curNode.lChild == None and curNode.data[0] in OPERATOR:
                curNode.lChild = node
                node.setParent(curNode)
                curNode = node
                break
            else:
                curNode = curNode.parent
        pointer += 1
    return root

def prefixFromTree(tree):
    output = []
    output_tag = []
    node = tree
    def traversePrefixFromTree(node):
        print node.data[1]
        output.append(node.data[0])
        output_tag.append(node.data[1])

        if node.lChild != None:
            traversePrefixFromTree( node.lChild)
        if node.rChild != None:
            traversePrefixFromTree( node.rChild)
        
        return
    traversePrefixFromTree(node)
    return output,output_tag

def infixToPostfix(data,tags):
    stack = []
    stack_tag = []
    output = []
    output_tag = []

    def ifOperator(d,t):
            if len(stack) == 0 or stack[len(stack)-1] == '(' or PREC[stack[len(stack)-1]] < PREC[d]:
                stack.append(d)
                stack_tag.append(t)
            elif PREC[stack[len(stack)-1]] > PREC[d]:
                output.append(stack.pop())
                output_tag.append(stack_tag.pop())
                ifOperator(d,t)
            else:
                output.append(stack.pop())
                output_tag.append(stack_tag.pop())
                stack.append(d)
                stack_tag.append(t)

    for d,t in zip(data,tags):
        if d in OPERATOR:
            ifOperator(d,t)
        elif d == '(':
            stack.append(d)
            stack_tag.append(t)
        elif d == ')':
            while True:
                toAppend = stack.pop()
                toAppend_tag = stack_tag.pop()
                if toAppend != '(':
                    output.append(toAppend)
                    output_tag.append(toAppend_tag)
                else:
                    break
        else:
            output.append(d)
            output_tag.append(t)

    for op,t in zip(stack[::-1],stack_tag[::-1]):
        output.append(op)
        output_tag.append(t)
    #print "".join(output)
    return output,output_tag

def toString(content):
    block = [content[x][0] for x in xrange(len(content))]
    return " ".join(block)