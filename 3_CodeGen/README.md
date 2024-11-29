# HANA Programming Language Parser
by Ella Kim (yk3040) and Je Yang (jy3342)


## 1. AST Processing to Generate MIPS Assembly
- `AST Traversal`: Traverse the AST in a depth-first manner, identifying language constructs like function definitions, control statements, and expressions.
- `Code Generation`: Convert each node into a corresponding lower-level representation, such as pseudocode or machine-readable code. Nodes like FuncDefNode, IfNode, etc., are translated into corresponding lower-level language syntax.
- `Optimization`: Simplify expressions and remove redundant or dead code during code generation to improve efficiency.



## 2. Execution Pipeline
After generating the lower-level code, a pipeline is used to execute the generated code to produce the required output. The pipeline includes the following steps:
- `Code Generation`: Translate the AST to a lower-level language.
- `Interpreter`: Interpret and execute the generated code using a custom interpreter. This interpreter processes each line of the generated code and performs the corresponding action.
- `Logging`: Log any errors during execution, and track which stage of the pipeline generated an error (e.g., syntax error during parsing, semantic error during interpretation).



## 3. Sample Input Programs and Expected Outputs
### Sample 1
**Input file**
```
x = 10                                                // x = 10
출력(x)                                                // print(x)
```
**Output code**
