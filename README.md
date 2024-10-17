# COMS4115-PLT
Hana - Language for translating all syntax and commands are expressed in the Korean language to Python style code

**Please `cd 1_LexicalAnalyzer` or direct to `1_LexicalAnalyzer` direcotry for Readme on Lexer information.** 

## Token Types

### 1. **Keyword Tokens**  
   These tokens correspond to the following keywords in Python:
   - `함수` (function)
   - `만약에` (if)
   - `아니면` (else)
   - `동안에` (while)
   - `반환` (return)
   - `출력` (print)
   - `진실` (true)
   - `거짓` (false)
   - `널` (null)
#### Data Structure
   - `배열` (Array): `길이` (len()), `추가` (append), `뽑기` (pop), `확장` (extend), `정렬` (sort)
   - `딕셔너리` (Dictionary): `키` (key()), `아이템` (item())
#### Math Function
   - `랜덤` (random)
   - `절댓값` (abs)
   - `최소값` (min)
   - `최대값` (max)

### 2. **Identifier Tokens**
We are allowing identifiers to consist of valid Hangul characters, digits, and underscores. The digits must precede with an underscore. These identifiers will include Hangul Jamo, Compatibility Jamo, and pre-composed Hangul syllables. The Unicode ranges for each of these types of characters are:
   -  \u1100-\u11FF: Hangul Jamo (used for composing Hangul syllables).
   - \u3130-\u318F: Hangul Compatibility Jamo (used for compatibility with older encodings).
   - \uAC00-\uD7AF: Pre-composed Hangul syllables (the most commonly used Korean characters in modern texts).
We also allow:
   - Digits (0-9) only after an underscore.
   - Underscore (`_`) only between two valid Hangul characters or digits. 

Regular Expression:
`[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF][[_][0-9]*[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]*]*`
Valid examples:
한국어_123
한국어_1_한
한국어_한_1

### 3. **Operator Tokens**:
   - '+', '-', '*', '**', '/', '%', '=', '==', '!=', '<', '>', '<=', '>='
#### Arithmetic Operators
- Order of Evaluation
Arithmetic operators follow the PEMDAS rule. This means parentheses `()` have the highest precedence, followed by multiplication `*`, division `/`, and modulus `%`, which take precedence over addition `+` and subtraction `-`.
- Addition and Subtraction
We permit the use of the addition and subtraction operator between two variables of type `int` or `float`, or between two expressions that result in `int` or `float`. The operands on both sides of the operator can be of different type (i.e. can be `int + float`). 
We do not support the shorthand operators `++` or `--` for incrementing or decrementing by 1.
- Multiplication and Division
Only allow int and float (traditional mathematical multiplication and division)
Division: quotient remain and remainder is removed
- Modulo 
Modulo (%) returns the division’s remainder. Only use int. 
#### Boolean/Equivalence Operators: <, >, <=, >=, !=, ==
#### Logical Operators: `그리고` (and), `이거나` (or)

### 4. **Delimiter Tokens**
- `(`: Open Parenthesis
- `)`: Close Parenthesis
- `{`: Open Brace
- `}`: Close Brace
- `,`: Comma
- `:`: Colon (used after control flow statements like `만약` or after function definitions like `함수`)
- `;`: Semicolon (optional terminator, for clarity or separation)

**Regex Rule**: `[\(\)\{\},:;]`

### 5. **Comments/String Tokens**
- Comment Tokens:
Single-line Comments: In Hana, comments can start with a hash # (similar to Python).
Everything following # on that line is ignored by the interpreter.
Pattern: #.* (matches everything after # to the end of the line).
- String Tokens:
String Literals: Strings are enclosed in double quotes ("). All characters within the quotes are considered part of the string until the closing quote.
Pattern: "(?:[^"\\]|\\.)*" (matches any sequence of characters between double quotes, allowing escaped characters like \").

### 6. **Number Tokens**
- Integer: Sequence of digits: '[0-9]+'
- Float: Sequence of digits, decimal point, sequence of digits: '[0-9]+.[0-9]+'

Je Yang (jy3342) and Ella Kim (yk3040)
