# HANA Programming Language Parser
by Ella Kim (yk3040) and Je Yang (jy3342)


## 1. Context-Free-Grammar
- digit0    : 0-9
- digit     : 1-9
- letter    : \u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF | a-z | A-Z
- otherchar : |!”%&/()=+-*#><;,^.][\n \t
- char      : letter | otherchar | digit0

- int       : '0' | digit+digit0*
- float     : digit0+ '.' digit0+
- num       : ('-')?(float | int)
- bool      : 'True' | '진실' | 'False' | '거짓'
- null      : 'NULL' | '널'
- var       : letter ([[_digit0*] | [_letter]])*
- qString   : '"' (char)* '"'
- commentLine   : '#' (char)*

- obj       : var | num | qString | bool | null | list | listElem

- list      : '[' (listExpr)? ']'
- listElem  : var '[' int ']'
- listExpr  : obj (',' obj)*

- operator  : '+' | '-' | '*' | '**' | '/' | '%' | condition
- condition : '&&' | '||' | '!=' | '==' | '<=' | '>=' | '>' | '<'

- assign    : var '=' expr

- expr      : pred (condition expr)?
- pred      : term ( ('+' | '-') pred)?
- term      : baseExpr ( ('*' | '/' | '/.' | '%') term)?
- baseExpr  : obj | '(' expr ')'

### Function Definition and Control Structures
- funcDef   : '함수' var '(' (var (',' var)*)? ')' '{' funcBody '}'
- funcBody  : (line ENDLINE)* (returnLine ENDLINE)?
- returnLine: '반환' expr

- ifLine    : '만약에' ifCond '{' ifBody '}' (elsePart)?
- ifCond    : '(' expr ')'
- ifBody    : line (ENDLINE line)*

- elsePart  : '아니면' '{' line (ENDLINE line)* '}'

- loopLine  : '동안에' loopCond '{' loopBody '}'
- loopCond  : '(' expr ')'
- loopBody  : line (ENDLINE line)*

### Statements and Lines
- line      : assign | funcCall | ifLine | loopLine | breakLine | contLine | outputLine | cString
- funcCall  : var '(' (expr (',' expr)*)? ')'
- breakLine : 'break'
- contLine  : 'continue'
- outputLine: '출력' '(' qString (',' expr)* ')'

### Program
- program   : (funcDef | line | commentLine)*
