import sys
import lexer_2
import ast_node
from parser import Parser

class MIPSCodeGenerator:
    def __init__(self):
        self.code = []
        self.label_counter = 0
        self.stack_offset = 0  # Keeps track of the current stack offset
        self.variable_stack = {}  # Maps variable names to stack offsets

    def generate_label(self, base="label"):
        label = f"{base}_{self.label_counter}"
        self.label_counter += 1
        return label
    
    def allocate_stack(self, var_name):
        """Allocate stack space for a variable and update the stack offset."""
        if var_name not in self.variable_stack:
            self.stack_offset -= 4  # Decrement stack pointer for new variable (4 bytes per word)
            self.variable_stack[var_name] = self.stack_offset
            self.code.append(f"# Allocating space for variable {var_name}")
            self.code.append(f"sw $zero, {self.stack_offset}($sp)  # Initialize {var_name} to 0")

    def get_stack_offset(self, var_name):
        """Get the stack offset for a variable."""
        if var_name not in self.variable_stack:
            self.allocate_stack(var_name)  # Automatically allocate missing variables
        return self.variable_stack[var_name]
 
    def process_ast(self, node):
        if isinstance(node, ast_node.FuncDefNode):
            self.code.append(f"\n# Function {node.name}")
            self.code.append(f"{node.name}:")
            for stmt in node.body:
                self.process_ast(stmt)
            self.code.append("jr $ra  # Return from function")

        elif isinstance(node, ast_node.AssignNode):
            # Allocate space on the stack for the variable
            self.allocate_stack(node.var.name)
            self.process_ast(node.expr)
            stack_offset = self.get_stack_offset(node.var.name)
            self.code.append(f"sw $v0, {stack_offset}($sp)  # Store {node.var.name}")

        elif isinstance(node, ast_node.BinaryOpNode):
            self.process_ast(node.left)
            self.code.append("move $t1, $v0  # Save left operand")
            self.process_ast(node.right)
            if node.operator == "+":
                self.code.append("add $v0, $t1, $v0")
            elif node.operator == "-":
                self.code.append("sub $v0, $t1, $v0")
            elif node.operator == "*":
                self.code.append("mul $v0, $t1, $v0")
            elif node.operator == "/":
                self.code.append("div $v0, $t1, $v0")
            elif node.operator == "==":
                self.code.append("seq $v0, $t1, $v0")
            elif node.operator == "!=":
                self.code.append("sne $v0, $t1, $v0")
            elif node.operator == "<":
                self.code.append("slt $v0, $t1, $v0")
            elif node.operator == "<=":
                self.code.append("sle $v0, $t1, $v0")
            elif node.operator == ">":
                self.code.append("sgt $v0, $t1, $v0")
            elif node.operator == ">=":
                self.code.append("sge $v0, $t1, $v0")
       
        elif isinstance(node, ast_node.NumberNode):
            self.code.append(f"li $v0, {node.value}")

        elif isinstance(node, ast_node.IdentifierNode):
            stack_offset = self.get_stack_offset(node.name)
            self.code.append(f"lw $v0, {stack_offset}($sp)  # Load {node.name}")

        elif isinstance(node, ast_node.PrintNode):
            self.process_ast(node.expr)
            self.code.append("move $a0, $v0  # Move value to $a0 for printing")
            self.code.append("li $v0, 1  # Print integer syscall")
            self.code.append("syscall")

        elif isinstance(node, ast_node.IfNode):
            self.process_ast(node.condition)
            false_label = self.generate_label("false")
            self.code.append(f"beq $v0, $zero, {false_label}  # If condition is false, jump")
            for stmt in node.body:
                self.process_ast(stmt)
            if node.else_body:
                end_label = self.generate_label("end")
                self.code.append(f"j {end_label}  # Jump to end after true block")
                self.code.append(f"{false_label}:")
                for stmt in node.else_body:
                    self.process_ast(stmt)
                self.code.append(f"{end_label}:")
            else:
                self.code.append(f"{false_label}:")
                
        elif isinstance(node, ast_node.WhileNode):
            start_label = self.generate_label("start")
            end_label = self.generate_label("end")
            self.code.append(f"{start_label}:")
            self.process_ast(node.condition)
            self.code.append(f"beq $v0, $zero, {end_label}")
            for stmt in node.body:
                self.process_ast(stmt)
            self.code.append(f"j {start_label}")
            self.code.append(f"{end_label}:")
    def get_code(self):
        return "\n".join(self.code)
  

class Pipeline:
    def __init__(self, source_code):
        self.source_code = source_code
        self.lexer = lexer_2.Lexer()
        self.generator = MIPSCodeGenerator()

    def process(self):
        # Step 1: Lexical Analysis
        # Step 2: Syntactic Analysis
        parser = Parser(self.source_code)
        ast = parser.parse()

        # Step 3: Code Generation
        for node in ast:
            self.generator.process_ast(node)

        # Step 4: Output the generated code
        generated_code = self.generator.get_code()
        with open("output.asm", "w") as output_file:
            output_file.write(generated_code)
        print("Generated MIPS code saved to output.asm")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mips_codegen.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    pipeline = Pipeline(source_code)
    pipeline.process()
