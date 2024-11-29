import pdb
import sys
import re

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
        if isinstance(node, ast_node.ErrorNode):
            # If an ErrorNode is encountered, stop code generation
            self.code.append(f"# Error encountered: {node.message}")
            return False

        if isinstance(node, ast_node.FuncDefNode):
            self.code.append(f"\n# Function {node.name}")
            self.code.append(f"{node.name}:")
            for stmt in node.body:
                if not self.process_ast(stmt):
                    return False
            self.code.append("jr $ra  # Return from function")

        elif isinstance(node, ast_node.AssignNode):
            # Allocate space on the stack for the variable
            self.allocate_stack(node.var.name)
            if not self.process_ast(node.expr):
                return False
            stack_offset = self.get_stack_offset(node.var.name)
            self.code.append(f"sw $v0, {stack_offset}($sp)  # Store {node.var.name}")

        elif isinstance(node, ast_node.BinaryOpNode):
            if not self.process_ast(node.left):
                return False
            self.code.append("move $t1, $v0  # Save left operand")
            if not self.process_ast(node.right):
                return False
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
            if not self.process_ast(node.expr):
                return False
            self.code.append("move $a0, $v0  # Move value to $a0 for printing")
            self.code.append("li $v0, 1  # Print integer syscall")
            self.code.append("syscall")

        elif isinstance(node, ast_node.IfNode):
            if not self.process_ast(node.condition):
                return False
            false_label = self.generate_label("false")
            self.code.append(f"beq $v0, $zero, {false_label}  # If condition is false, jump")
            for stmt in node.body:
                if not self.process_ast(stmt):
                    return False
            if node.else_body:
                end_label = self.generate_label("end")
                self.code.append(f"j {end_label}  # Jump to end after true block")
                self.code.append(f"{false_label}:")
                for stmt in node.else_body:
                    if not self.process_ast(stmt):
                        return False
                self.code.append(f"{end_label}:")
            else:
                self.code.append(f"{false_label}:")
                
        elif isinstance(node, ast_node.WhileNode):
            start_label = self.generate_label("start")
            end_label = self.generate_label("end")
            self.code.append(f"{start_label}:")
            if not self.process_ast(node.condition):
                return False
            self.code.append(f"beq $v0, $zero, {end_label}")
            for stmt in node.body:
                if not self.process_ast(stmt):
                    return False
            self.code.append(f"j {start_label}")
            self.code.append(f"{end_label}:")
        return True

    def get_code(self):
        return "\n".join(self.code)
  

class Pipeline:
    def __init__(self, source_code, output_filename):
        self.generator = MIPSCodeGenerator()
        self.source_code = source_code
        self.output_filename = output_filename

    def process(self):
        # Step 1: Lexical Analysis
        # Step 2: Syntactic Analysis
        parser = Parser(self.source_code)
        ast = parser.parse()

        # Step 3: Code Generation
        for node in ast:
            if not self.generator.process_ast(node):
                break

        # Step 4: Output the generated code
        generated_code = self.generator.get_code()

        with open(self.output_filename, "w") as output_file:
            output_file.write(generated_code)
        print(f"Generated MIPS code saved to {self.output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mips_codegen.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Extract sample number from input filename
    match = re.search(r'sample(\d+)\.txt$', input_file)
    if match:
        sample_number = match.group(1)
        output_filename = f"samples_output/output{sample_number}.asm"
    else:
        output_filename = "samples_output/output.asm"  # Default output name if no sample number is found

    pipeline = Pipeline(source_code, output_filename)
    pipeline.process()
