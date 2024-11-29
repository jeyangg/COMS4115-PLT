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

    def generate_label(self, base="label"):
        label = f"{base}_{self.label_counter}"
        self.label_counter += 1
        return label

    def process_ast(self, node):
        if isinstance(node, ast_node.FuncDefNode):
            self.code.append(f"\n# Function {node.name}")
            self.code.append(f"{node.name}:")
            for stmt in node.body:
                self.process_ast(stmt)
            self.code.append("jr $ra  # Return from function")
        elif isinstance(node, ast_node.AssignNode):
            self.process_ast(node.expr)
            self.code.append(f"sw $v0, {node.var.name}")
        elif isinstance(node, ast_node.BinaryOpNode):
            self.process_ast(node.left)
            self.code.append("move $t1, $v0")
            self.process_ast(node.right)
            if node.operator == "+":
                self.code.append("add $v0, $t1, $v0")
            elif node.operator == "-":
                self.code.append("sub $v0, $t1, $v0")
            elif node.operator == "*":
                self.code.append("mul $v0, $t1, $v0")
            elif node.operator == "/":
                self.code.append("div $v0, $t1, $v0")
        elif isinstance(node, ast_node.NumberNode):
            self.code.append(f"li $v0, {node.value}")
        elif isinstance(node, ast_node.IdentifierNode):
            self.code.append(f"lw $v0, {node.name}")
        elif isinstance(node, ast_node.IfNode):
            self.process_ast(node.condition)
            false_label = self.generate_label("false")
            self.code.append(f"beq $v0, $zero, {false_label}")
            for stmt in node.body:
                self.process_ast(stmt)
            if node.else_body:
                end_label = self.generate_label("end")
                self.code.append(f"j {end_label}")
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
        elif isinstance(node, ast_node.PrintNode):
            self.process_ast(node.expr)
            self.code.append("li $v0, 1  # Print integer syscall")
            self.code.append("syscall")

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
            self.generator.process_ast(node)

        # Step 4: Output the generated code
        generated_code = self.generator.get_code()

        with open(self.output_filename, "w") as output_file:
            output_file.write(generated_code)
        print("Generated MIPS code saved to output.asm")


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
