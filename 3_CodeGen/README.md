# HANA Programming Language Parser
by Ella Kim (yk3040) and Je Yang (jy3342)

## 1. AST Processing to Generate MIPS Assembly
- `AST Traversal`: Traverse the AST in a depth-first manner, identifying language constructs like function definitions, control statements, and expressions.
- `Code Generation`: Convert each node into a corresponding lower-level representation, such as pseudocode or machine-readable code. Nodes like FuncDefNode, IfNode, etc., are translated into corresponding lower-level language syntax.
- **Implementation**:
The MIPSCodeGenerator class handles the AST traversal and converts nodes into MIPS instructions. Each node type (e.g., AssignNode, IfNode, WhileNode) is processed by a specific method, generating code for arithmetic operations, function calls, conditionals, and loops.

## 2. Execution Pipeline
After generating the lower-level code, a pipeline is used to execute the generated code to produce the required output. The pipeline includes the following steps:
- `Code Generation`: Translate the AST to a lower-level language.
- `Interpreter`: Interpret and execute the generated code using a custom interpreter. This interpreter processes each line of the generated code and performs the corresponding action.
- `Logging`: Log any errors during execution, and track which stage of the pipeline generated an error (e.g., syntax error during parsing, semantic error during interpretation).



## 3. Sample Input Programs and Expected Outputs
### Sample 1
**Input file**
```
x = 10                                               
출력(x)                                              
```
**Output code**

### Sample 2
**Input file**
```
x = 5
만약에 x == 10 {
    출력("x는 10입니다.")
}
아니면 {
    출력("x는 10이 아닙니다.")
}
```
**Output code**

### Sample 3
**Input file**
```
딕셔너리 연산기 = {}

함수 더하기(x, y) {
    연산기[x] = x + y
}

함수 빼기(x, y) [
    반환 x - y
]

함수 지수(x, y) {
	반환 x ** z
}

더하기(4, 5)
지수(2, 6)
출력(연산기.키())
```
**Output code**


### Sample 4
**Input file**
```
배열 아이디 = []
x = 4

동안에 (x < 5) {
	x = x + 1
    아이디.추가(x)
}

아이디_원소_0 = 아이디.뽑기()
```
**Output Code**

### Sample 5
**Input file**
```
함수 피보나치(n) {
    만약에 (n <= 1) {
        반환 n
    } 아니면 {
        반환 피보나치(n - 1) + 피보나치(n - 2)
    }
}

함수 주요_함수() {
    결과 = 10
    한국어_123_변수 = 5.5
    테스트_변수 = 진실
    널_테스트 = 널

    만약에 (테스트_변수 == 진실 그리고 한국어_123 < 결과) {
        출력("조건이 참입니다!")
    } 아니면 {
        출력("조건이 거짓입니다.")
    }

    카운터 = 0
    동안에 (카운터 < 5..5) {
        출력(피보나치(카운터))
        카운터 = 카운터 + 1
    }

    수학_결과 = (결과 * 한국어_123) % 3 + 2 - 1
    출력("수학 결과: ", 수학_결과)

    # '이것은 주석입니다'
    # -> 이것 또한 주석입니다'
    문자열_테스트 = "이것은 '문자열'입니다."
    출력(문자열_테스트)
}
문자열_테스트 = "이것은 바뀐 문자열입니다.'
```
**Output code**

## 4. Video
Link here: 
