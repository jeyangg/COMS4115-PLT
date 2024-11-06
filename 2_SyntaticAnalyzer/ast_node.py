class ASTNode:
    def __repr__(self):
        return self._repr(0)

    def _repr(self, indent):
        return "ASTNode()"

# Basic Expression Nodes
class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def _repr(self, indent):
        indent_str = "    " * indent
        return "{}IdentifierNode(name='{}')".format(indent_str, self.name)

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def _repr(self, indent):
        indent_str = "    " * indent
        return "{}NumberNode(value={})".format(indent_str, self.value)

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def _repr(self, indent):
        indent_str = "    " * indent
        return "{}StringNode(value='{}')".format(indent_str, self.value)

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def _repr(self, indent):
        indent_str = "    " * indent
        return "{}BooleanNode(value={})".format(indent_str, self.value)

class NullNode(ASTNode):
    def _repr(self, indent):
        indent_str = "    " * indent
        return "{}NullNode()".format(indent_str)

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}BinaryOpNode(\n"
            "{}    left=\n{}\n"
            "{}    operator='{}'\n"
            "{}    right=\n{}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.left._repr(indent + 2),
            indent_str, self.operator,
            indent_str, self.right._repr(indent + 2),
            indent_str
        )

class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}UnaryOpNode(\n"
            "{}    operator='{}'\n"
            "{}    operand=\n{}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.operator,
            indent_str, self.operand._repr(indent + 2),
            indent_str
        )

# Statements
class AssignNode(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}AssignNode(\n"
            "{}    var=\n{}\n"
            "{}    expr=\n{}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.var._repr(indent + 2),
            indent_str, self.expr._repr(indent + 2),
            indent_str
        )

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def _repr(self, indent):
        indent_str = "    " * indent
        body_repr = "\n".join(stmt._repr(indent + 2) for stmt in self.body)
        else_repr = (
            "None" if not self.else_body else "\n".join(stmt._repr(indent + 2) for stmt in self.else_body)
        )
        return (
            "{}IfNode(\n"
            "{}    condition=\n{}\n"
            "{}    body=[\n{}\n{}    ]\n"
            "{}    else_body={}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.condition._repr(indent + 2),
            indent_str, body_repr,
            indent_str,
            indent_str, else_repr,
            indent_str
        )

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def _repr(self, indent):
        indent_str = "    " * indent
        body_repr = "\n".join(stmt._repr(indent + 2) for stmt in self.body)
        return (
            "{}WhileNode(\n"
            "{}    condition=\n{}\n"
            "{}    body=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.condition._repr(indent + 2),
            indent_str, body_repr,
            indent_str,
            indent_str
        )

class FuncDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def _repr(self, indent):
        indent_str = "    " * indent
        body_repr = "\n".join(stmt._repr(indent + 2) for stmt in self.body)
        return (
            "{}FuncDefNode(\n"
            "{}    name='{}'\n"
            "{}    params={}\n"
            "{}    body=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.name,
            indent_str, self.params,
            indent_str, body_repr,
            indent_str,
            indent_str
        )

class ReturnNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}ReturnNode(\n"
            "{}    expr=\n{}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.expr._repr(indent + 2),
            indent_str
        )

class FuncCallNode(ASTNode):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def _repr(self, indent):
        indent_str = "    " * indent
        args_repr = "\n".join(arg._repr(indent + 2) for arg in self.args)
        return (
            "{}FuncCallNode(\n"
            "{}    func_name='{}'\n"
            "{}    args=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.func_name,
            indent_str, args_repr,
            indent_str,
            indent_str
        )

# List and Elements
class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def _repr(self, indent):
        indent_str = "    " * indent
        elements_repr = "\n".join(element._repr(indent + 2) for element in self.elements)
        return (
            "{}ListNode(\n"
            "{}    elements=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str,
            elements_repr,
            indent_str,
            indent_str
        )

class ListElemNode(ASTNode):
    def __init__(self, list_var, index):
        self.list_var = list_var
        self.index = index

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}ListElemNode(\n"
            "{}    list_var=\n{}\n"
            "{}    index=\n{}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.list_var._repr(indent + 2),
            indent_str, self.index._repr(indent + 2),
            indent_str
        )

# Output and Comments
class PrintNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}PrintNode(\n"
            "{}    expr=\n{}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.expr._repr(indent + 2),
            indent_str
        )

class CommentNode(ASTNode):
    def __init__(self, text):
        self.text = text

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}CommentNode(\n"
            "{}    text='{}'\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.text,
            indent_str
        )
