import pdb
import re
import enum
import sys

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
        return ('Token({}, {})'.format(self.type, self.value))



class Lexer:
    def __init__(self):
        self.input = ""
        self.position = 0       # for simple string input
        self.line = 1           # for code with multiple lines
        self.column = 1
        self.hana_keywords = ["함수", "만약에", "만약", "아니면", "동안에", "반환", "출력", "진실", "거짓", "널"]
        self.hana_logical = ["그리고", "이거나"]
        self.hana_delimiter = []


    def lookahead(self):
        # reach to the end of the input
        if self.position >= len(self.input): 
            return None

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

        elif char == '"':
            return self.handle_string(char)
        
        elif char == '#':
            return self.handle_string(char)

        elif char in '+-*=!<>':
            return self.handle_operator(char)

        elif char in '(){}[]':
            return self.handle_delimiter(char) 
        
        else:
            return self.handle_identifier(char)

        return Token(TokenType.ERROR, "Unexpected character: {}".format(char))


    def handle_digit(self, digit_src):
        value = digit_src
        while True:
            if self.position < len(self.input):
                char = self.input[self.position]
            else:
                char = None

            if char is None or (not char.isdigit() and char != '.'):
                break
            value += self.lookahead()
        return Token(TokenType.NUMBER, value)


    def handle_operator(self, op_src):
        value = op_src
        if op_src in '=!<>':
            value += self.lookahead()
        return Token(TokenType.OPERATOR, value)
    

    def handle_string(self, str_src):
        value = str_src
        while True:
            char = self.lookahead()
            if char is None:
                return Token(TokenType.ERROR, "Unterminated string")
            value += char
            if char == '"':
                break
        return Token(TokenType.STRING, value)
    

    def handle_comment(self, str_src):
        value = str_src
        while self.position < len(self.input):
            char = self.input[self.position]
            if char == '\n':
                break
            value += self.lookahead()
        return Token(TokenType.STRING, value)
    
    def handle_delimiter(self, delimiter):
        start_column = self.column - 1
        if delimiter in '({[':
            self.hana_delimiter.append((delimiter, self.line, start_column))
        elif delimiter in ')}]':
            if self.hana_delimiter:
                last_delimiter = self.hana_delimiter[-1][0]
                if (last_delimiter == '(' and delimiter == ')') or \
                   (last_delimiter == '{' and delimiter == '}') or \
                   (last_delimiter == '[' and delimiter == ']'):
                    self.hana_delimiter.pop()
                else:
                    return Token(TokenType.ERROR, f"Mismatched delimiter: expected closing {last_delimiter}, found {delimiter}")
            else:
                return Token(TokenType.ERROR, f"Unmatched closing delimiter: {delimiter}")
        return Token(TokenType.DELIMITER, delimiter)


    def handle_identifier(self, id_src):
        value = id_src
        while True:
            if self.position < len(self.input):
                char = self.input[self.position]
            else:
                char = None

            if char is None or not (char.isalnum() or char == '_'):
                break
            value += self.lookahead()

        if value in self.hana_keywords:
            return Token(TokenType.KEYWORD, value)
        elif value in self.hana_logical:
            return Token(TokenType.OPERATOR, value)
        return Token(TokenType.IDENTIFIER, value)



def main(input_file):
    if len(sys.argv) != 2:
        print("Usage: python3.11 lexer.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # print(source_code)
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
        for token in tokens:
            print(token)

    except FileNotFoundError:
        print("Error: File {} not found.".format(input_file))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e))
        sys.exit(1)



if __name__ == "__main__":
    main(sys.argv[1])