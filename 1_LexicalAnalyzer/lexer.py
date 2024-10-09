import pdb
import re
import enum

class TokenType:
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    DELIMITER = 'DELIMITER'
    STRING = 'STRING'
    ERROR = 'ERROR'



class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'



class Lexer:
    def __init__(self):
        self.input = ""
        self.position = 0       # for simple string input
        self.line = 1           # for code with multiple lines
        self.column = 1


    def lookahead(self):
        # reach to the end of the input
        if self.position >= len(self.input): return None

        char = self.input[self.position]
        self.position += 1
        self.column += 1

        # reach to the end of the line
        if char == '\n':
            self.line += 1
            self.column = 1
        return char


    def tokenize(self, input_string):
        self.input = input_string
        tokens = []
        while True:
            token = self.tokenize_nxt()
            if token is None:
                break
            tokens.append(token)
        return tokens
    

    def tokenize_nxt(self):
        char = self.lookahead()   
        if char is None:
            return None
        # else:
        #     print("tokenize_nxt > char: ", char, type(char), ord(char))

        if char.isspace():
            return self.tokenize_nxt()

        elif char.isdigit():
            return self.handle_digit(char)

        elif char in '+-*=!<>':
            return self.handle_operator(char)

        elif char in '(){}[]':
            return Token(TokenType.DELIMITER, char)
        
        # else:
        #     return self.handle_identifier(char)

        return Token(TokenType.ERROR, f"Unexpected character: {char}")


    def handle_digit(self, digit_src):
        value = digit_src
        while True:
            char = self.lookahead()
            if char is None or (not char.isdigit() and char != '.'):
                break
            value += self.next_char()
        return Token(TokenType.NUMBER, value)


    def handle_operator(self, op_src):
        value = op_src
        if op_src in '=!<>':
            value += self.lookahead()
        return Token(TokenType.OPERATOR, value)
    




def main():
    test_string = ["만약 임시 < 5", "임시_123 > 1 동안에"]
    
    lexer = Lexer()
    
    for test in test_string:
        tokens = lexer.tokenize(test)
        print(f"Input: {test}")
        print("Tokens:")
        for token in tokens:
            print(f"  {token}")

if __name__ == "__main__":
    main()