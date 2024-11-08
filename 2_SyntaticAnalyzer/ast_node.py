import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'NanumGothic'  # Make sure you have installed Nanum Gothic or another Korean font


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
        assert isinstance(left, ASTNode), "Expected ASTNode for left, got {}".format(type(left).__name__)
        assert isinstance(right, ASTNode), "Expected ASTNode for right, got {}".format(type(right).__name__)
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
        return (
            "{}IfNode(\n"
            "{}    condition=\n{}\n"
            "{}    body=[\n{}\n{}    ]\n"
            "{}    else_body={}\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.condition._repr(indent + 2),
            indent_str, self.body,
            indent_str,
            indent_str, self.else_body,
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
        return (
            "{}FuncCallNode(\n"
            "{}    func_name='{}'\n"
            "{}    args=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.func_name,
            indent_str, self.args,
            indent_str,
            indent_str
        )

# Dictionary and items
class DictNode(ASTNode):
    def __init__(self, name, key=None, value=None):
        self.name = name
        self.key = key
        self.value = value

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}DictNode(\n"
            "{}    name={}\n"
            "{}    key=[{}]\n"
            "{}    value=[{}]\n"
            "{})"
        ).format(
            indent_str,
            indent_str,
            self.name,
            indent_str,
            self.key,
            indent_str,
            self.value,
            indent_str
        )

class DictAssignNode:
    def __init__(self, dict, key, value):
        self.dict = dict
        self.key = key
        self.value = value

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            f"{indent_str}DictAssignNode(\n"
            f"{indent_str}    dict={self.dict.name},\n"
            f"{indent_str}    key={self.key},\n"
            f"{indent_str}    value={self.value}\n"
            f"{indent_str})"
        )
    
# List and Elements
class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}ListNode(\n"
            "{}    elements=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str,
            self.elements,
            indent_str,
            indent_str
        )

class MethodCallNode(ASTNode):
    def __init__(self, list, method, args):
        self.list = list
        self.method = method
        self.args = args

    def _repr(self, indent):
        indent_str = "    " * indent
        return (
            "{}MethodCallNode(\n"
            "{}    list='{}'\n"
            "{}    method='{}'\n"
            "{}    args=[\n{}\n{}    ]\n"
            "{})"
        ).format(
            indent_str,
            indent_str, self.list,
            indent_str, self.method,
            indent_str, self.args,
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

class ErrorNode(ASTNode):
    def __init__(self, message, context=None):
        self.message = message
        self.context = context

    def __repr__(self):
        message_repr = "!!! Message={} !!!".format(self.message)
        context_repr = "\nExpectedContext:\n{}".format(self.context) if self.context else ""
        return "ErrorNode(\n{}{}\n)".format(message_repr, context_repr)


class ASTVisualizer:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_counter = 0  # To keep track of unique node labels

    def add_node(self, node, parent_label=None):
        # Create a unique label for each node based on its type and counter
        current_label = f"{type(node).__name__}_{self.node_counter}"
        label_text = repr(node) if not isinstance(node, (FuncDefNode, BinaryOpNode, DictAssignNode, ReturnNode, IfNode)) else f"{type(node).__name__}"
        self.graph.add_node(current_label, label=label_text)
        self.node_counter += 1

        # Add an edge from the parent to the current node
        if parent_label:
            self.graph.add_edge(parent_label, current_label)

        # Recursively add child nodes based on the node type
        if isinstance(node, FuncDefNode):
            params_label = f"Params: {node.params}"
            params_node_label = f"Params_{self.node_counter}"
            self.graph.add_node(params_node_label, label=params_label)
            self.node_counter += 1
            self.graph.add_edge(current_label, params_node_label)

            for stmt in node.body:
                self.add_node(stmt, current_label)
        elif isinstance(node, DictAssignNode):
            self.add_node(node.value, current_label)
        elif isinstance(node, BinaryOpNode):
            self.add_node(node.left, current_label)
            self.add_node(f"Operator: {node.operator}", current_label)
            self.add_node(node.right, current_label)
        elif isinstance(node, ReturnNode):
            self.add_node(node.expr, current_label)
        elif isinstance(node, IfNode):
            # Add condition node with full condition details
            condition_label = f"Condition_{self.node_counter}"
            condition_text = f"Condition: {repr(node.condition)}"
            self.graph.add_node(condition_label, label=condition_text)
            self.node_counter += 1
            self.graph.add_edge(current_label, condition_label)

            # Add if body statements directly
            for stmt in node.body:
                self.add_node(stmt, condition_label)

            # Add else body if present
            if node.else_body:
                else_body_label = f"ElseBody_{self.node_counter}"
                self.graph.add_node(else_body_label, label="Else Body")
                self.node_counter += 1
                self.graph.add_edge(condition_label, else_body_label)
                for stmt in node.else_body:
                    self.add_node(stmt, else_body_label)
        elif isinstance(node, ErrorNode):
            # Only add the ErrorNode itself without visiting its context
            return



    def plot(self):
        # Get labels for nodes
        labels = nx.get_node_attributes(self.graph, 'label')
        
        # Create a layout and draw the graph in a vertical tree structure using a spring layout
        pos = nx.circular_layout(self.graph) 
        plt.figure(figsize=(12, 10))
        nx.draw(self.graph, pos, labels=labels, with_labels=True, node_size=5000, 
                node_color='powderblue', font_weight='bold', font_size=8, arrows=True)
        plt.show()