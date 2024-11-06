class ASTNode:
    pass

# Basic Expression Nodes
class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "IdentifierNode(name='{}')".format(self.name)

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "NumberNode(value={})".format(self.value)

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "StringNode(value='{}')".format(self.value)

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "BooleanNode(value={})".format(self.value)

class NullNode(ASTNode):
    def __init__(self):
        pass

    def __repr__(self):
        return "NullNode()"

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return "BinaryOpNode(left={}, operator='{}', right={})".format(self.left, self.operator, self.right)

class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return "UnaryOpNode(operator='{}', operand={})".format(self.operator, self.operand)

# Statements
class AssignNode(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "AssignNode(var={}, expr={})".format(self.var, self.expr)

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return "IfNode(condition={}, body={}, else_body={})".format(self.condition, self.body, self.else_body)

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return "WhileNode(condition={}, body={})".format(self.condition, self.body)

class FuncDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return "FuncDefNode(name='{}', params={}, body={})".format(self.name, self.params, self.body)

class ReturnNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "ReturnNode(expr={})".format(self.expr)

class FuncCallNode(ASTNode):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return "FuncCallNode(func_name='{}', args={})".format(self.func_name, self.args)

# List and Elements
class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return "ListNode(elements={})".format(self.elements)

class ListElemNode(ASTNode):
    def __init__(self, list_var, index):
        self.list_var = list_var
        self.index = index

    def __repr__(self):
        return "ListElemNode(list_var={}, index={})".format(self.list_var, self.index)

# Output and Comments
class PrintNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "PrintNode(expr={})".format(self.expr)

class CommentNode(ASTNode):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "CommentNode(text='{}')".format(self.text)
