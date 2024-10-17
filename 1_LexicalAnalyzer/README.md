# HANA Programming Language Lexer
by Ella Kim (yk3040) and Je Yang (jy3342)


## 1. Lexical Grammar
Please refer to the root directory `README.md` for more details on the token types. 

### Token Types
1. **Keyword**: Reserved words in the language.
   - **Examples**: `함수`, `반환`, `출력`
   - **Rule**: Exact matches with predefined reserved words.
   
2. **Identifier**: Names of variables, functions, etc.
   - **Examples**: `x`, `변수`
   - **Rule**: An identifier starts with an alphabetic/Korean character and can contain letters, digits, and underscores after.

3. **Number**: Numeric literals, including integers and floating-point numbers.
   - **Examples**: `123`, `45.67`
   - **Rule**: Consists of digits, optionally containing one decimal point.

4. **Operator**: Arithmetic, comparison, and logical operators.
   - **Examples**: `+`, `-`, `=`, `==`, `<=`, `>=`, `!=`, `%`, `*`
   - **Rule**: Matches valid operator symbols.

5. **Delimiter**: Punctuation symbols used for grouping and separating.
   - **Examples**: `()`, `{}`, `[]`, `,`, `:`, `.`
   - **Rule**: Any grouping or punctuation symbols.

6. **String**: A sequence of characters enclosed in double quotes.
   - **Examples**: `"안녕!"`
   - **Rule**: Enclosed by `"`.

7. **Comment**: Text following the `#` symbol, ignored by the lexer.
   - **Rule**: Any text following a `#` until the end of the line.

---
## 2. Scanning Algorithm

Our scanning algorithm is built as a deterministic finite automaton (DFA). The lexer processes the input program one character at a time, and based on the current character and state, it determines the type of token and transitions between states.

At a high level, the lexer starts in the `START` state and reads characters sequentially. Depending on the type of character (whether it's a letter, digit, operator, etc.), the lexer transitions into different states, processes the token, and then returns to `START` to continue scanning the next token.

### 2a. State Transition (DFA) 
The HANA lexer operates as a DFA, which means it transitions between predefined states based on the input character. Here's how the lexer transitions through various states:

#### Key States

1. **START**: This is the initial state of the lexer, where it begins processing each character. The lexer determines what type of token it is encountering (e.g., identifier, number, operator) and transitions to the appropriate state.
   
   - **Transitions from START**:
     - If a letter is encountered, transition to `IN_IDENTIFIER`.
     - If a digit is encountered, transition to `IN_NUMBER`.
     - If an operator is encountered, transition to `IN_OPERATOR`.
     - If a `"` (double quote) is encountered, transition to `IN_STRING`.
     - If a `#` (comment) is encountered, transition to `IN_STRING` to handle the comment.
     - If a delimiter (`()[]{},:`) is encountered, transition to `IN_DELIMITER`.

2. **IN_IDENTIFIER**: The lexer is reading an identifier or keyword. It continues reading characters until a non-alphanumeric character or underscore is encountered.
   
   - **Transitions from IN_IDENTIFIER**:
     - If an alphanumeric character or `_` is encountered, stay in `IN_IDENTIFIER`.
     - If a non-alphanumeric character is encountered, return to `START`.

3. **IN_NUMBER**: The lexer is reading a number. It continues reading digits, possibly allowing a single decimal point.
   
   - **Transitions from IN_NUMBER**:
     - If a digit is encountered, stay in `IN_NUMBER`.
     - If a `.` is encountered and no decimal has been seen yet, stay in `IN_NUMBER` to handle floating-point numbers.
     - If a non-digit is encountered, return to `START`.

4. **IN_OPERATOR**: The lexer is reading an operator such as `+`, `-`, `*`, `=`, etc. It may combine characters to form compound operators (e.g., `==`, `<=`, `!=`).
   
   - **Transitions from IN_OPERATOR**:
     - If an operator is encountered, stay in `IN_OPERATOR`.
     - If no more operator characters are found, return to `START`.

5. **IN_STRING**: The lexer is reading a string or comment. Strings are enclosed in double quotes (`"`), and comments begin with a `#` and extend to the end of the line.
   
   - **Transitions from IN_STRING**:
     - If a closing double quote (`"`) or newline (for comments) is encountered, return to `START`.
     - If the end of the input is reached without closing a string, the lexer raises an error for an unterminated string.

6. **IN_DELIMITER**: The lexer is reading a delimiter such as `(`, `)`, `{`, `}`, `[`, `]`, `,`, `:`.
   
   - **Transitions from IN_DELIMITER**:
     - Once a delimiter is identified, the lexer returns to `START`.

7. **ERROR**: If the lexer encounters an unrecognized or invalid character, it transitions to the `ERROR` state and raises an error.

---

#### Detailed State Transition Example

For an input like:

```plaintext
함수 더하기(x, y):
    반환 x + y
```

The lexer will transition through the following states:

1. **START**: Encounters `함수`, identifies it as a keyword, transitions to `IN_IDENTIFIER`, and then back to `START`.
2. **START**: Encounters `더하기`, identifies it as an identifier, transitions to `IN_IDENTIFIER`, and then back to `START`.
3. **START**: Encounters `(`, identifies it as a delimiter, transitions to `IN_DELIMITER`, and then back to `START`.
4. **START**: Encounters `x`, identifies it as an identifier, transitions to `IN_IDENTIFIER`, and then back to `START`.
5. **START**: Encounters `,`, identifies it as a delimiter, transitions to `IN_DELIMITER`, and then back to `START`.
6. **START**: Encounters `y`, identifies it as an identifier, transitions to `IN_IDENTIFIER`, and then back to `START`.
7. **START**: Encounters `:`, identifies it as a delimiter, transitions to `IN_DELIMITER`, and then back to `START`.
8. **START**: Encounters `반환`, identifies it as a keyword, transitions to `IN_IDENTIFIER`, and then back to `START`.
9. **START**: Encounters `x`, identifies it as an identifier, transitions to `IN_IDENTIFIER`, and then back to `START`.
10. **START**: Encounters `+`, identifies it as an operator, transitions to `IN_OPERATOR`, and then back to `START`.
11. **START**: Encounters `y`, identifies it as an identifier, transitions to `IN_IDENTIFIER`, and then back to `START`.

---

### 2b. Token Output Format

The tokens are output in the format: `<TokenType, TokenValue>`. For example, parsing the input:

```plaintext
함수 더하기(x, y):
    반환 x + y
```

Will produce the following output:
```plaintext
<TokenType.KEYWORD, 함수>
<TokenType.IDENTIFIER, 더하기>
<TokenType.DELIMITER, (>
<TokenType.IDENTIFIER, x>
<TokenType.DELIMITER, ,>
<TokenType.IDENTIFIER, y>
<TokenType.DELIMITER, )>
<TokenType.DELIMITER, :>
<TokenType.KEYWORD, 반환>
<TokenType.IDENTIFIER, x>
<TokenType.OPERATOR, +>
<TokenType.IDENTIFIER, y>
```

---

#### Implementation Steps

1. **Read Input Character-by-Character**: The lexer reads the input program one character at a time using the `lookahead` function, keeping track of the current line and column numbers.

2. **Identify Token Type**: Based on the character, the lexer determines what kind of token is being read (e.g., identifier, number, operator) and transitions to the corresponding state (e.g., `IN_IDENTIFIER`, `IN_NUMBER`, etc.).

3. **Transition Between States**: While in a particular state, the lexer continues reading characters until the end of the token is reached (e.g., reading digits for numbers or characters for identifiers). Once a complete token is identified, the lexer returns to the `START` state to process the next token.

4. **Handle Lexical Errors**: If an invalid character is encountered, the lexer transitions to the `ERROR` state and outputs an error message indicating the problematic character and its position in the input.

5. **Token Output**: After each token is identified, it is stored in the list of tokens, which is later output by the lexer in the format `<TokenType, TokenValue>`.

---

### 2c. Lexical Error Handling

The lexer handles lexical errors, such as
- **Unrecognized characters**: If the lexer encounters characters like `@`, `$`, etc., they are classified as errors.

Example of an error:
```plaintext
<TokenType.ERROR, Unexpected character: @ at line 5, column 3>
```

## 3. Token Handling
- `lookahead`
    - Get the character of input and track its position (line, column) until we meet the end of the file
- `handle_digit`
    - Process numeric tokens
    - Possible next state: START, NUMBER (followed by dot), IDENTIFIER (followed by alpha)
- `handle_operator`
    - Process operator tokens
    - Possible next state: START
- `handle_string`
    - Process string tokens
    - Possible next state: START (If the string is closed with paired "), STRING
    - Note that if the opened string is not closed, HANA lexer will keep recognizing the following tokens as a string (Sample 5). 
- `handle_comment`
    - Process comment tokens as a string
    - Possible next state: START (When the comment is finished with "\n"), STRING
- `handle_delimiter`
    - Process delimiter tokens
    - Possible next state: START, DELIMITER
- `handle_identifier`
    - Process identifiers and keywords
    - Possible next state: START, KEYWORD, OPERATOR (logic words), IDENTIFIER 


## 4. Sample Input Programs and Expected Outputs
### Execution
Ensure you have Python 3.7+ installed on your system.  `./run_lexer.sh`

### Sample 1
**Input file**
```
x = 10                                                  // x = 10
y = 1..1                                                // y = 1..1
출력(x/y)                                                // print(x/y)
```

**Expected Output**
```
Token(TokenType.IDENTIFIER, x)
Token(TokenType.OPERATOR, =)
Token(TokenType.NUMBER, 10)
Token(TokenType.IDENTIFIER, y)
Token(TokenType.OPERATOR, =)
Token(TokenType.NUMBER, 1)
Token(TokenType.DELIMITER, .)
Token(TokenType.DELIMITER, .)
Token(TokenType.NUMBER, 1)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, x)
Token(TokenType.OPERATOR, /)
Token(TokenType.DELIMITER, ))
```

### Sample 2
**Input file**
```
만약에 x == 10:                                         // if (x == 10):
    출력("x는 10입니다.")                                 //    print("x is equal ot 10")
아니면:                                                 // else:
    출력("x는 10이 아닙니다.")                             //   print("x is not equal to 10")
```
**Expected Output**
```
Token(TokenType.KEYWORD, 만약에)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.OPERATOR, ==)
Token(TokenType.NUMBER, 10)
Token(TokenType.DELIMITER, :)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.STRING, "x는 10입니다.")
Token(TokenType.DELIMITER, ))
Token(TokenType.KEYWORD, 아니면)
Token(TokenType.DELIMITER, :)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.STRING, "x는 10이 아닙니다.")
Token(TokenType.DELIMITER, ))
```

### Sample 3
**Input file**
```
딕셔너리 연산기 = {}                                    // dictionary arithmetic = {}

함수 더하기(x, y):                                     // function addition(x, y):
    연산기[x] = x + y                                 //    arithmetic[x] = x + y

함수 지수{x, y):                                      // function power{x, y):
    연산기[x] = x ** y                                //    arithmetic[x] = x ** y

더하기(4, 5)                                          // addition(x, y)
지수(2, 6)                                           // power(2, 6)
출력(연산기.키())                                       // print(arithmetic.key())
출력(연산기.아이템(@))                                   // print(arithmetic.item(@))
```     
**Expected Output**
```
Token(TokenType.KEYWORD, 딕셔너리)
Token(TokenType.IDENTIFIER, 연산기)
Token(TokenType.OPERATOR, =)
Token(TokenType.DELIMITER, {)
Token(TokenType.DELIMITER, })
Token(TokenType.KEYWORD, 함수)
Token(TokenType.IDENTIFIER, 더하기)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, x)
Token(TokenType.DELIMITER, ,)
Token(TokenType.IDENTIFIER, y)
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, :)
Token(TokenType.IDENTIFIER, 연산기)
Token(TokenType.DELIMITER, [)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.DELIMITER, ])
Token(TokenType.OPERATOR, =)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.OPERATOR, +)
Token(TokenType.IDENTIFIER, y)
Token(TokenType.KEYWORD, 함수)
Token(TokenType.IDENTIFIER, 지수)
Token(TokenType.DELIMITER, {)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.DELIMITER, ,)
Token(TokenType.IDENTIFIER, y)
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, :)
Token(TokenType.IDENTIFIER, 연산기)
Token(TokenType.DELIMITER, [)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.DELIMITER, ])
Token(TokenType.OPERATOR, =)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.OPERATOR, **)
Token(TokenType.IDENTIFIER, y)
Token(TokenType.IDENTIFIER, 더하기)
Token(TokenType.DELIMITER, ()
Token(TokenType.NUMBER, 4)
Token(TokenType.DELIMITER, ,)
Token(TokenType.NUMBER, 5)
Token(TokenType.DELIMITER, ))
Token(TokenType.IDENTIFIER, 지수)
Token(TokenType.DELIMITER, ()
Token(TokenType.NUMBER, 2)
Token(TokenType.DELIMITER, ,)
Token(TokenType.NUMBER, 6)
Token(TokenType.DELIMITER, ))
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 연산기)
Token(TokenType.DELIMITER, .)
Token(TokenType.KEYWORD, 키)
Token(TokenType.DELIMITER, ()
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, ))
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 연산기)
Token(TokenType.DELIMITER, .)
Token(TokenType.KEYWORD, 아이템)
Token(TokenType.DELIMITER, ()
Token(TokenType.ERROR, Unexpected character: @ at line 12, column 13)
Token(TokenType.ERROR, Unexpected character: ))
Token(TokenType.ERROR, Unexpected character: ))
```

### Sample 4
**Input file**
```
배열 아이디 = []                                         // list id = []

(아이디.길이() < 10) 동안에:                               // while(len(id) < 10):
    원소 = 랜덤()                                        //    element = random()
    아이디.추가(원소)                                     //    id.append(element)
                                                      //
아이디_원소_0 = 아이디.뽑기()                               // element_0 = id.pop()
3원소 = 아이디.뽑기(3)                                    // 3element = tmp_1_id.pop(3)
```
**Expected Output**
```
Token(TokenType.KEYWORD, 배열)
Token(TokenType.IDENTIFIER, 아이디)
Token(TokenType.OPERATOR, =)
Token(TokenType.DELIMITER, [)
Token(TokenType.DELIMITER, ])
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 아이디)
Token(TokenType.DELIMITER, .)
Token(TokenType.KEYWORD, 길이)
Token(TokenType.DELIMITER, ()
Token(TokenType.DELIMITER, ))
Token(TokenType.OPERATOR, <)
Token(TokenType.NUMBER, 10)
Token(TokenType.DELIMITER, ))
Token(TokenType.KEYWORD, 동안에)
Token(TokenType.DELIMITER, :)
Token(TokenType.IDENTIFIER, 원소)
Token(TokenType.OPERATOR, =)
Token(TokenType.KEYWORD, 랜덤)
Token(TokenType.DELIMITER, ()
Token(TokenType.DELIMITER, ))
Token(TokenType.IDENTIFIER, 아이디)
Token(TokenType.DELIMITER, .)
Token(TokenType.KEYWORD, 추가)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 원소)
Token(TokenType.DELIMITER, ))
Token(TokenType.IDENTIFIER, 아이디_원소_0)
Token(TokenType.OPERATOR, =)
Token(TokenType.IDENTIFIER, 아이디)
Token(TokenType.DELIMITER, .)
Token(TokenType.KEYWORD, 뽑기)
Token(TokenType.DELIMITER, ()
Token(TokenType.DELIMITER, ))
Token(TokenType.IDENTIFIER, 3원소)
Token(TokenType.OPERATOR, =)
Token(TokenType.IDENTIFIER, 아이디)
Token(TokenType.DELIMITER, .)
Token(TokenType.KEYWORD, 뽑기)
Token(TokenType.DELIMITER, ()
Token(TokenType.NUMBER, 3)
Token(TokenType.DELIMITER, ))
```

### Sample 5
**Input file**
```
함수 피보나치(n) {                                              // function Fibonacci(n){
    만약에 n <= 1 {                                           //    if n <= 1 {
        반환 n                                               //         return n
    } 아니면 {                                                //    } else {
        반환 피보나치(n - 1) + 피보나치(n - 2)                    //        return Fibonacci(n-1) + Fibonacci(n-2) 
    }                                                       //    }
}                                                           // }

함수 주요_함수() {                                              // function main_function(){
    결과 = 10                                                 //    result = 10
    한국어_123_변수 = 5.5                                       //    korean_123_variable = 5.5
    테스트_변수 = 진실                                           //    test_variable = True
    널_테스트 = 널                                              //    null_test = Null
                                                             //
    만약에 테스트_변수 == 진실 그리고 한국어_123 < 결과 {              //    if test_varaible == True and korean_123 < result {
        출력("조건이 참입니다!")                                  //        print("condition is True!")
    } 아니면 {                                                 //   } else {
        출력("조건이 거짓입니다.")                                 //       print("condition is False!")
    }                                                        //   }
                                                             //
    카운터 = 0                                                 //   counter = 0
    동안에 카운터 < 5 {                                         //   while (counter < 5){
        출력(피보나치(카운터))                                    //       print(Fibonacci(counter))
        카운터 = 카운터 + 1                                     //       counter = counter + 1
    }                                                        //   }
                                                             //
    수학_결과 = (결과 * 한국어_123) % 3 + 2 - 1                   // math_result = (result * korean_123) % 3 + 2 - 1 
    출력("수학 결과: ", 수학_결과)                                // print("math result: ", math_result)
                                                            //
    # '이것은 주석입니다'                                        // # 'This is comment'
    # -> 이것 또한 주석입니다'                                    // # -> This is also comment'
    문자열_테스트 = "이것은 '문자열'입니다."                         // string_test = "This is 'string'."
    출력("문자열_테스트)                                         // print("string_test)
}                                                            // }
```

**Expected Output**
```
Token(TokenType.KEYWORD, 함수)
Token(TokenType.IDENTIFIER, 피보나치)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, n)
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, {)
Token(TokenType.KEYWORD, 만약에)
Token(TokenType.IDENTIFIER, n)
Token(TokenType.OPERATOR, <=)
Token(TokenType.NUMBER, 1)
Token(TokenType.DELIMITER, {)
Token(TokenType.KEYWORD, 반환)
Token(TokenType.IDENTIFIER, n)
Token(TokenType.DELIMITER, })
Token(TokenType.KEYWORD, 아니면)
Token(TokenType.DELIMITER, {)
Token(TokenType.KEYWORD, 반환)
Token(TokenType.IDENTIFIER, 피보나치)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, n)
Token(TokenType.OPERATOR, -)
Token(TokenType.NUMBER, 1)
Token(TokenType.DELIMITER, ))
Token(TokenType.OPERATOR, +)
Token(TokenType.IDENTIFIER, 피보나치)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, n)
Token(TokenType.OPERATOR, -)
Token(TokenType.NUMBER, 2)
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, })
Token(TokenType.DELIMITER, })
Token(TokenType.KEYWORD, 함수)
Token(TokenType.IDENTIFIER, 주요_함수)
Token(TokenType.DELIMITER, ()
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, {)
Token(TokenType.IDENTIFIER, 결과)
Token(TokenType.OPERATOR, =)
Token(TokenType.NUMBER, 10)
Token(TokenType.IDENTIFIER, 한국어_123_변수)
Token(TokenType.OPERATOR, =)
Token(TokenType.NUMBER, 5.5)
Token(TokenType.IDENTIFIER, 테스트_변수)
Token(TokenType.OPERATOR, =)
Token(TokenType.KEYWORD, 진실)
Token(TokenType.IDENTIFIER, 널_테스트)
Token(TokenType.OPERATOR, =)
Token(TokenType.KEYWORD, 널)
Token(TokenType.KEYWORD, 만약에)
Token(TokenType.IDENTIFIER, 테스트_변수)
Token(TokenType.OPERATOR, ==)
Token(TokenType.KEYWORD, 진실)
Token(TokenType.OPERATOR, 그리고)
Token(TokenType.IDENTIFIER, 한국어_123)
Token(TokenType.OPERATOR, <)
Token(TokenType.IDENTIFIER, 결과)
Token(TokenType.DELIMITER, {)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.STRING, "조건이 참입니다!")
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, })
Token(TokenType.KEYWORD, 아니면)
Token(TokenType.DELIMITER, {)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.STRING, "조건이 거짓입니다.")
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, })
Token(TokenType.IDENTIFIER, 카운터)
Token(TokenType.OPERATOR, =)
Token(TokenType.NUMBER, 0)
Token(TokenType.KEYWORD, 동안에)
Token(TokenType.IDENTIFIER, 카운터)
Token(TokenType.OPERATOR, <)
Token(TokenType.NUMBER, 5)
Token(TokenType.DELIMITER, {)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 피보나치)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 카운터)
Token(TokenType.DELIMITER, ))
Token(TokenType.DELIMITER, ))
Token(TokenType.IDENTIFIER, 카운터)
Token(TokenType.OPERATOR, =)
Token(TokenType.IDENTIFIER, 카운터)
Token(TokenType.OPERATOR, +)
Token(TokenType.NUMBER, 1)
Token(TokenType.DELIMITER, })
Token(TokenType.IDENTIFIER, 수학_결과)
Token(TokenType.OPERATOR, =)
Token(TokenType.DELIMITER, ()
Token(TokenType.IDENTIFIER, 결과)
Token(TokenType.OPERATOR, *)
Token(TokenType.IDENTIFIER, 한국어_123)
Token(TokenType.DELIMITER, ))
Token(TokenType.OPERATOR, %)
Token(TokenType.NUMBER, 3)
Token(TokenType.OPERATOR, +)
Token(TokenType.NUMBER, 2)
Token(TokenType.OPERATOR, -)
Token(TokenType.NUMBER, 1)
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.STRING, "수학 결과: ")
Token(TokenType.DELIMITER, ,)
Token(TokenType.IDENTIFIER, 수학_결과)
Token(TokenType.DELIMITER, ))
Token(TokenType.STRING, # '이것은 주석입니다')
Token(TokenType.STRING, # -> 이것 또한 주석입니다')
Token(TokenType.IDENTIFIER, 문자열_테스트)
Token(TokenType.OPERATOR, =)
Token(TokenType.STRING, "이것은 '문자열'입니다.")
Token(TokenType.KEYWORD, 출력)
Token(TokenType.DELIMITER, ()
Token(TokenType.STRING, "문자열_테스트)
})
```


