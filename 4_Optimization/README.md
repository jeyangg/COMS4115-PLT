# HANA Programming Language Optimizer
by Ella Kim (yk3040) and Je Yang (jy3342)

## 1. AST Processing to Generate MIPS Assembly

## 2. Code Optimization
After the code generator translates an Abstract Syntax Tree (AST) into MIPS assembly code, optimizer performs below strategies to reduce execution time, to minimize resource utilization and to improve overall system performance.
- `Constant Folding` simplifies constant expressions at compile time to reduce runtime computation. During AST traversal, if a binary operation involves two constants, the result is computed at compile time. The simplified value replaces the expression in the generated code.

- `Algebraic Simplification` applies mathematical identities to simplify expressions (operations including zero and one), reducing instruction count. These are handle during AST processing.

- `Dead Code Elimination` removes code that does not affect the program's observable behavior, reducing unnecessary intsructions. AST nodes corresponding to unreachable or unused code will not be processed like code after unconditional jump or return statement, or assignments to variables that are never used.

- `Register Tracking` avoids redundant loading of constants into registers, thereby reducing the number of instructions executed. A `register_state` dictionary tracks the current value stored in each register. Before loading a constant into a register, the generator checks if the value is already present. If the value is already in the register, the redundant load is skipped.



## 3. Sample Input Programs and Expected Outputs
### Execution (!! Take a look into our [demo video]())
Ensure you have Python 3.7+ installed on your system.  `./run_optcodegen.sh samples/sample{#}.txt` The output optimized assembly code will be saved as samples_output/sample{#}.asm.

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
