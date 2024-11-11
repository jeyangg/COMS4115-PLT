import pdb
import re
import enum
import sys

import ast_node
import lexer_2

class Parser:
    def __init__(self, source_code):
        self.lexer = lexer_2.Lexer()
        self.tokens = self.lexer.tokenize(source_code)  # Tokenize directly here
        self.position = 0

    def current_token(self):
        while self.position < len(self.tokens) and self.tokens[self.position].type == lexer_2.TokenType.COMMENT:
            self.position += 1
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1
        while self.position < len(self.tokens) and self.tokens[self.position].type == lexer_2.TokenType.COMMENT:
            self.position += 1
    
    def expect(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token.type == expected_type and (expected_value is None or token.value == expected_value):
            self.advance()
            return token
        else:
            expected_val = expected_value if expected_value else expected_type
            actual_val = token.value if token else 'EOF'
            raise SyntaxError("Expected {}, got {}".format(expected_val, actual_val))

    def parse(self):
        ast = []
        while self.current_token():
            token = self.current_token()
            if token.type == lexer_2.TokenType.KEYWORD:
                if token.value == "함수":
                    ast.append(self.parse_func_def())
                elif token.value == "출력":
                    ast.append(self.parse_print())
                elif token.value == "만약에": 
                    ast.append(self.parse_if())
                elif token.value == "동안에":
                    ast.append(self.parse_while())
                elif token.value == "배열":
                    ast.append(self.parse_array_declaration())
                elif token.value == "딕셔너리":
                    ast.append(self.parse_dict_declaration())
                else:
                    raise SyntaxError("Unexpected top-level token {}".format(token.value))
            elif token.type == lexer_2.TokenType.IDENTIFIER:
                identifier = token
                self.advance()
                if self.current_token() and self.current_token().type == lexer_2.TokenType.DELIMITER and self.current_token().value == "(":
                    ast.append(self.parse_func_call(identifier.value))
                else:
                    self.position -= 1
                    ast.append(self.parse_assign())
            elif token.type == lexer_2.TokenType.KEYWORD and token.value == "clear":
                self.advance()  # Move to the next token after 'clear'
                continue  # Skip the 'clear' token and continue parsing
            else:
                raise SyntaxError("Unexpected top-level token {}".format(token.value))
        return ast

    # Array Declaration Parsing
    def parse_array_declaration(self):
        self.expect(lexer_2.TokenType.KEYWORD, "배열")
        array_name = self.expect(lexer_2.TokenType.IDENTIFIER).value
        self.expect(lexer_2.TokenType.OPERATOR, "=")
        self.expect(lexer_2.TokenType.DELIMITER, "[")
        self.expect(lexer_2.TokenType.DELIMITER, "]")
        return ast_node.ListNode(array_name)
    
    # Dictionary Declaration Parsing
    def parse_dict_declaration(self):
        self.expect(lexer_2.TokenType.KEYWORD, "딕셔너리")
        array_name = self.expect(lexer_2.TokenType.IDENTIFIER).value
        self.expect(lexer_2.TokenType.OPERATOR, "=")
        self.expect(lexer_2.TokenType.DELIMITER, "{")
        self.expect(lexer_2.TokenType.DELIMITER, "}")
        return ast_node.DictNode(array_name)
    
    def parse_method_call(self, list):
        self.expect(lexer_2.TokenType.DELIMITER, ".")
        method = self.expect(lexer_2.TokenType.KEYWORD).value
        self.expect(lexer_2.TokenType.DELIMITER, "(")
        args = []
        if self.current_token().type != lexer_2.TokenType.DELIMITER or self.current_token().value != ")":
            args.append(self.parse_expr())
            while self.current_token().value == ",":
                self.advance()
                args.append(self.parse_expr())
        self.expect(lexer_2.TokenType.DELIMITER, ")")
        return ast_node.FuncCallNode(method, args)

    def parse_element_call(self, obj_name):
        self.expect(lexer_2.TokenType.DELIMITER, "[")
        index = self.parse_expr()
        self.expect(lexer_2.TokenType.DELIMITER, "]")
        self.expect(lexer_2.TokenType.OPERATOR, "=")
        value = self.parse_expr()
        return ast_node.DictAssignNode(ast_node.DictNode(obj_name), index, value)
    
    def parse_func_call(self, func_name):
        self.expect(lexer_2.TokenType.DELIMITER, "(")
        args = []
        while self.current_token() and self.current_token().type != lexer_2.TokenType.DELIMITER:
            args.append(self.parse_expr())
            if self.current_token() and self.current_token().value == ",":
                self.advance()  # Move past the comma
        self.expect(lexer_2.TokenType.DELIMITER, ")")  # Expect closing parenthesis
        return ast_node.FuncCallNode(func_name, args)


    # Parse Expressions
    def parse_expr(self):
        left = self.parse_pred()
        while self.current_token() and self.current_token().value in ["&&", "||", '!=', '==', '<=', '>=', '>', '<', "그리고", "이거나", ","]:
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
        while self.current_token() and self.current_token().value in ["*", "**", "/", "%"]:
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
            # Check if the string is unterminated
            if not (token.value.startswith('"') and token.value.endswith('"')) and not (token.value.startswith("'") and token.value.endswith("'")):
                error_node = ast_node.ErrorNode("Unterminated string literal", token.value)
                self.advance()
                return error_node
            
            # If the string is properly terminated, proceed normally
            self.advance()
            return ast_node.StringNode(token.value)
        elif token.type == lexer_2.TokenType.IDENTIFIER:
            self.advance()
            identifier = token.value
            if self.current_token() and self.current_token().value == ".":
                return self.parse_method_call(identifier)  # Array method calls
            if self.current_token() and self.current_token().value == "(":
                return self.parse_func_call(identifier)
            return ast_node.IdentifierNode(identifier)
        elif token.type == lexer_2.TokenType.KEYWORD:
            if token.value == "랜덤":
                self.advance()  # Move past "랜덤"
                if self.current_token() and self.current_token().value == "(":
                    self.advance()  # Move past "("
                    self.expect(lexer_2.TokenType.DELIMITER, ")")  # Expect closing ")"
                    return ast_node.FuncCallNode(token.value, [])
                else:
                    # Return ErrorNode if "(" is not found
                    context = "Expected '(' after '랜덤'"
                    return ast_node.ErrorNode("Expected '('", context)
            elif token.value == "진실":
                self.advance()
                return ast_node.BooleanNode(True)
            elif token.value == "거짓":
                self.advance()
                return ast_node.BooleanNode(False)
            elif token.value == "널":
                self.advance()
                return ast_node.NullNode()
        elif token.value == "(":
            self.advance()
            expr = self.parse_expr()
            self.expect(lexer_2.TokenType.DELIMITER, ")")
            return expr
        else:
            context = "Unexpected token: {}".format(token.value)
            error_node = ast_node.ErrorNode("Unexpected token", context)
            return error_node
        
    # Parse If Statement
    def parse_if(self):
        self.expect(lexer_2.TokenType.KEYWORD, "만약에")
        # Parse the condition directly after "만약에"
        condition = self.parse_expr() 
        self.expect(lexer_2.TokenType.DELIMITER, "{") 
        body = self.parse_body()
        self.expect(lexer_2.TokenType.DELIMITER, "}")  
        
        # Handle the optional "아니면" (else) part
        else_body = None
        if self.current_token() and self.current_token().value == "아니면":
            self.advance()
            self.expect(lexer_2.TokenType.DELIMITER, "{") 
            else_body = self.parse_body()
            self.expect(lexer_2.TokenType.DELIMITER, "}")
            
        return ast_node.IfNode(condition, body, else_body)
    
    def parse_while(self):
        self.expect(lexer_2.TokenType.KEYWORD, "동안에")
        condition = self.parse_expr() 
        self.expect(lexer_2.TokenType.DELIMITER, "{") 
        body = self.parse_body()
        self.expect(lexer_2.TokenType.DELIMITER, "}")  
        return ast_node.WhileNode(condition, body)
    
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

        # Handle incorrect delimiter for function body
        try:
            self.expect(lexer_2.TokenType.DELIMITER, "{")
            body = self.parse_body()

            try:
                self.expect(lexer_2.TokenType.DELIMITER, "}")
            except SyntaxError as e:
                # If the closing brace is missing, create an error node with the current function context.
                message = "Expected function closed with '}', got EOF"
                context = ast_node.FuncDefNode(func_name, params, body)
                return ast_node.ErrorNode(message, context)
            return ast_node.FuncDefNode(func_name, params, body)
        except:
            # handling wrong delimiter open
            closer = "}"
            if self.current_token().value == "[":
                closer = "]"
            elif self.current_token().value == "(":
                closer = ")"
            message = "Unexpected function open"
            self.advance()
            body = []
            while self.current_token() and self.current_token().value != closer:
                body.append(self.parse_statement())
            context = ast_node.FuncDefNode(func_name, params, body)

            self.advance()
            return ast_node.ErrorNode(message, context)

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
                return self.parse_print()
        elif token.type == lexer_2.TokenType.IDENTIFIER:
            self.advance()
            if self.current_token().value == ".":
                return self.parse_method_call(token.value)  # Array method calls
            elif self.current_token().value == "[":
                return self.parse_element_call(token.value)  # element method calls
            elif self.current_token().value == "=":
                self.position -= 1
                return self.parse_assign() 
        raise SyntaxError("Unexpected token {}".format(token.value))

    def parse_assign(self):
        var = self.expect(lexer_2.TokenType.IDENTIFIER).value
        self.expect(lexer_2.TokenType.OPERATOR, "=")
        expr = self.parse_expr()
        return ast_node.AssignNode(ast_node.IdentifierNode(var), expr)

    def parse_print(self):
        self.expect(lexer_2.TokenType.KEYWORD, "출력")
        self.expect(lexer_2.TokenType.DELIMITER, "(")
        expr = self.parse_expr()
        self.expect(lexer_2.TokenType.DELIMITER, ")")
        return ast_node.PrintNode(expr)

    
# Main function to use the Parser class
def main(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        parser = Parser(source_code)
        ast = parser.parse()
        visualizer = ast_node.ASTVisualizer()

        # Print the generated AST
        print("Generated AST:")
        print(ast)

        for node in ast:
            visualizer.add_node(node)
        visualizer.plot()

    except FileNotFoundError:
        print("Error: File '{}' not found.".format(input_file))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py <input_file>")
        sys.exit(1)

    main(sys.argv[1])