# HANA Programming Language Lexer
by Ella Kim (yk3040) and Je Yang (jy3342)

## Implementation Steps
### State transition (DFA)
### Token Handling
### Lexical Error Handling
1. Appearance of illegal characters (backslash, @, $)
2. Unterminated string except comment
3. Invalid variable name like starting with number or number following without '_' (Only "한국어_123", "한국어_1_한", and "한국어_한_1" can be accepted)

## Execution
Ensure you have Python 3.7+ installed on your system.

`./run_lexer.sh`

## Sample Input and Output
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
Token(TokenType.ERROR, Unexpected identifier pattern: '3원소' at line 8, column 4)
Token(TokenType.ERROR, Unexpected character:  )
Token(TokenType.ERROR, Unexpected character: =)
Token(TokenType.ERROR, Unexpected character:  )
Token(TokenType.ERROR, Unexpected character: 임)
Token(TokenType.ERROR, Unexpected character: 시)
Token(TokenType.ERROR, Unexpected character: _)
Token(TokenType.ERROR, Unexpected character: 1)
Token(TokenType.ERROR, Unexpected character: _)
Token(TokenType.ERROR, Unexpected character: 아)
Token(TokenType.ERROR, Unexpected character: 이)
Token(TokenType.ERROR, Unexpected character: 디)
Token(TokenType.ERROR, Unexpected character: .)
Token(TokenType.ERROR, Unexpected character: 뽑)
Token(TokenType.ERROR, Unexpected character: 기)
Token(TokenType.ERROR, Unexpected character: ()
Token(TokenType.ERROR, Unexpected character: 3)
Token(TokenType.ERROR, Unexpected character: ))
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
    # -> 이것 또한 주석입니다                                     // # -> This is also comment
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
Token(TokenType.ERROR, Unterminated string)
```