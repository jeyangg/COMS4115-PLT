import pdb
import re
import enum
import sys

class LexerState(enum.Enum):
    START = 'START'
    IN_KEYWORD = 'IN_KEYWORD'
    IN_IDENTIFIER = 'IN_IDENTIFIER'
    IN_NUMBER = 'IN_NUMBER'
    IN_OPERATOR = 'IN_OPERATOR'
    IN_DELIMITER = 'IN_DELIMITER'
    IN_STRING = 'IN_STRING'
    ERROR = 'ERROR'

class TokenType(enum.Enum):
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
        self.state = LexerState.START
        self.input = ""
        self.position = 0       # for simple string input
        self.line = 1           # for code with multiple lines
        self.column = 1
        self.hana_keywords = ["함수", "만약에", "만약", "아니면", "동안에", "반환", "출력", "진실", "거짓", "널"]
        self.hana_logical = ["그리고", "이거나"]
        self.hana_list = ["배열", "길이", "추가", "뽑기", "확장", "정렬"]
        self.hana_dictionary = ["딕셔너리", "키", "아이템"]
        self.hana_math = ["랜덤", "절댓값", "최소값", "최대값"]
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


    def transition_state(self, new_state):
        # print("Transitioning from {} to {}".format(self.state, new_state))
        self.state = new_state


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
        
        if self.state == LexerState.START:
            if char.isspace():
                return self.tokenize_nxt()  # Skip whitespace
            elif char.isdigit():
                self.transition_state(LexerState.IN_NUMBER)
                return self.handle_digit(char)
            elif char.isalpha():
                self.transition_state(LexerState.IN_IDENTIFIER)
                return self.handle_identifier(char)
            elif char == '"':
                self.transition_state(LexerState.IN_STRING)
                return self.handle_string(char)
            elif char == '#':
                self.transition_state(LexerState.IN_STRING)
                return self.handle_comment(char)
            elif char in '+-*=!<>%/':
                self.transition_state(LexerState.IN_OPERATOR)
                return self.handle_operator(char)
            elif char in '(){}[],:.':
                self.transition_state(LexerState.IN_DELIMITER)
                return self.handle_delimiter(char) 
            else:
                self.transition_state(LexerState.ERROR)
                return Token(TokenType.ERROR, "Unexpected character: {} at line {}, column {}".format(char, self.line, self.column))

        elif self.state == LexerState.IN_NUMBER:
            return self.handle_digit(char)
        
        elif self.state == LexerState.IN_IDENTIFIER:
            return self.handle_identifier(char)
        
        elif self.state == LexerState.IN_STRING:
            return self.handle_string(char)
        
        elif self.state == LexerState.IN_OPERATOR:
            self.transition_state(LexerState.START)
            return self.handle_operator(char)

        elif self.state == LexerState.IN_DELIMITER:
            self.transition_state(LexerState.START)
            return self.handle_delimiter(char)
        
        self.transition_state(LexerState.ERROR)
        return Token(TokenType.ERROR, "Unexpected character: {}".format(char))


    def handle_digit(self, digit_src):
        value = digit_src
        dot_encountered = False
        is_error = False  # Flag to indicate if there's an error in the digit sequence

        while True:
            if self.position < len(self.input):
                char = self.input[self.position]
            else:
                char = None

            if char is None:
                break

            if char == '.' and not dot_encountered:
                dot_encountered = True
                self.position += 1
                next_char = self.input[self.position] if self.position < len(self.input) else None
                if next_char == '.':
                    self.transition_state(LexerState.START)
                    self.position -= 1
                    return Token(TokenType.NUMBER, value)
                elif next_char.isdigit():
                    value += '.'
                else:
                    self.transition_state(LexerState.START)
                    return Token(TokenType.NUMBER, value)
            elif char == '.' and dot_encountered:
                self.transition_state(LexerState.START)
                return Token(TokenType.NUMBER, value)
            elif char.isdigit():
                value += self.lookahead()
            elif char.isalpha():
                value += self.lookahead()
                is_error = True  # Mark this as an error since a digit was followed by a letter
            else:
                self.transition_state(LexerState.START)
                break

        if is_error:
            self.transition_state(LexerState.START)
            return Token(TokenType.IDENTIFIER, value)

        return Token(TokenType.NUMBER, value)


    def handle_operator(self, op_src):
        value = op_src
        next_char = self.lookahead()
        if next_char is not None and next_char in '=<>*': 
            value += next_char
        self.transition_state(LexerState.START)
        return Token(TokenType.OPERATOR, value)
    

    def handle_string(self, str_src):
        value = str_src
        while True:
            char = self.lookahead()
            if char is None:
                self.transition_state(LexerState.START)
                break

            value += char
            if char == '"':
                self.transition_state(LexerState.START)
                break
        return Token(TokenType.STRING, value)
    

    def handle_comment(self, str_src):
        value = str_src
        while self.position < len(self.input):
            char = self.input[self.position]
            if char == '\n':
                self.transition_state(LexerState.START)
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
        self.transition_state(LexerState.START)
        return Token(TokenType.DELIMITER, delimiter)
    

    def handle_identifier(self, id_src):
        value = id_src
        is_error = False  # Flag to indicate if there's an error in the identifier

        while True:
            if self.position < len(self.input):
                char = self.input[self.position]
            else:
                char = None

            if char is None or not (char.isalnum() or char == '_'):
                self.transition_state(LexerState.START)
                break

            # Check if a digit immediately follows a Korean character, which should raise an error
            if char.isdigit() and not value[-1].isdigit() and not value[-1] == '_':
                is_error = True  # Mark this as an error
            value += self.lookahead()

        # Check if the identifier is a keyword or falls into other predefined categories
        if value in self.hana_keywords + self.hana_list + self.hana_dictionary + self.hana_math:
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