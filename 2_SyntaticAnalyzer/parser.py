import pdb
import re
import enum
import sys

import ast_node
import lexer_2

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1

    def expect(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token.type == expected_type and (expected_value is None or token.value == expected_value):
            self.advance()
            return token
        else:
            expected_val = expected_value if expected_value else expected_type
            actual_val = token.value if token else 'EOF'
            raise SyntaxError("Expected {}, got {}".format(expected_val,actual_val))

    # Parse Expressions
    def parse_expr(self):
        left = self.parse_pred()
        while self.current_token() and self.current_token().value in ["&&", "||"]:
            operator = self.current_token().value
            self.advance()
            right = self.parse_pred()
            left = ast_node.BinaryOpNode(left, operator, right)
        return left

    def parse_pred(self):
        left = self.parse_term()
        while self.current_token() and self.current_token().value in ["+", "-"]:
            operator = self.current_token().value
            self.advance()
            right = self.parse_term()
            left = ast_node.BinaryOpNode(left, operator, right)
        return left

    def parse_term(self):
        left = self.parse_base_expr()
        while self.current_token() and self.current_token().value in ["*", "/", "%"]:
            operator = self.current_token().value
            self.advance()
            right = self.parse_base_expr()
            left = ast_node.BinaryOpNode(left, operator, right)
        return left

    def parse_base_expr(self):
        token = self.current_token()
        if token.type == lexer_2.TokenType.NUMBER:
            self.advance()
            return ast_node.NumberNode(token.value)
        elif token.type == lexer_2.TokenType.STRING:
            self.advance()
            return ast_node.StringNode(token.value)
        elif token.type == lexer_2.TokenType.IDENTIFIER:
            self.advance()
            return ast_node.IdentifierNode(token.value)
        elif token.value == "(":
            self.advance()
            expr = self.parse_expr()
            self.expect(lexer_2.TokenType.DELIMITER, ")")
            return expr
        else:
            raise SyntaxError("Unexpected token {}".format(token.value))

    # Parse If Statement
    def parse_if(self):
        self.expect(lexer_2.TokenType.KEYWORD, "만약에")
        self.expect(lexer_2.TokenType.DELIMITER, "(")
        condition = self.parse_expr()
        self.expect(lexer_2.TokenType.DELIMITER, ")")
        self.expect(lexer_2.TokenType.DELIMITER, "{")
        body = self.parse_body()
        self.expect(lexer_2.TokenType.DELIMITER, "}")
        else_body = None
        if self.current_token() and self.current_token().value == "아니면":
            self.advance()
            self.expect(lexer_2.TokenType.DELIMITER, "{")
            else_body = self.parse_body()
            self.expect(lexer_2.TokenType.DELIMITER, "}")
        return ast_node.IfNode(condition, body, else_body)

    # Parse Function Definition
    def parse_func_def(self):
        self.expect(lexer_2.TokenType.KEYWORD, "함수")
        func_name = self.expect(lexer_2.TokenType.IDENTIFIER).value
        self.expect(lexer_2.TokenType.DELIMITER, "(")
        params = []
        if self.current_token().type == lexer_2.TokenType.IDENTIFIER:
            params.append(self.expect(lexer_2.TokenType.IDENTIFIER).value)
            while self.current_token().value == ",":
                self.advance()
                params.append(self.expect(lexer_2.TokenType.IDENTIFIER).value)
        self.expect(lexer_2.TokenType.DELIMITER, ")")
        self.expect(lexer_2.TokenType.DELIMITER, "{")
        body = self.parse_body()
        self.expect(lexer_2.TokenType.DELIMITER, "}")
        return ast_node.FuncDefNode(func_name, params, body)

    # Parse Body and Statements
    def parse_body(self):
        statements = []
        while self.current_token() and self.current_token().value != "}":
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        if token.type == lexer_2.TokenType.KEYWORD:
            if token.value == "만약에":
                return self.parse_if()
            elif token.value == "동안에":
                return self.parse_while()
            elif token.value == "반환":
                self.advance()
                return ast_node.ReturnNode(self.parse_expr())
            elif token.value == "출력":
                self.advance()
                self.expect(lexer_2.TokenType.DELIMITER, "(")
                expr = self.parse_expr()
                self.expect(lexer_2.TokenType.DELIMITER, ")")
                return ast_node.PrintNode(expr)
        elif token.type == lexer_2.TokenType.IDENTIFIER:
            return self.parse_assign()
        raise SyntaxError("Unexpected token {}".format(token.value))

    def parse_assign(self):
        var = self.expect(lexer_2.TokenType.IDENTIFIER).value
        self.expect(lexer_2.TokenType.OPERATOR, "=")
        expr = self.parse_expr()
        return ast_node.AssignNode(var, expr)

# Main Parsing Function
def parse(tokens):
    parser = Parser(tokens)
    ast = parser.parse_body()  # Starting point for parsing
    return ast
