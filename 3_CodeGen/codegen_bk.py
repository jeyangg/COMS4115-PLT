import os
import sys
import pdb
import re

import lexer_2
import ast_node
from parser import Parser

class MIPSCodeGenerator:
    def __init__(self):
        self.code = []
        self.label_counter = 0
        self.stack_offset = 4  # Keeps track of the current stack offset
        self.variable_stack = {}  # Maps variable names to stack offsets
        self.dictionary_map = {}
        self.data_section = []  # To store .data section declarations

    def generate_label(self, base="label"):
        label = f"{base}_{self.label_counter}"
        self.label_counter += 1
        return label
    
    def allocate_stack(self, var_name):
        """Allocate stack space for a variable and update the stack offset."""
        if var_name not in self.variable_stack:
            self.stack_offset -= 4  # Decrement stack pointer for new variable (4 bytes per word)
            self.variable_stack[var_name] = self.stack_offset
            self.code.append(f"sw {var_name}, {self.stack_offset}($sp)")

    def get_stack_offset(self, var_name):
        """Get the stack offset for a variable."""
        if var_name not in self.variable_stack:
            self.allocate_stack(var_name)  # Automatically allocate missing variables
        return self.variable_stack[var_name]
    
    def handle_func_def_node(self, node):
        self.code.append(f"{node.name}:")
        for stmt in node.body:
            self.process_ast(stmt)
        self.code.append("jr $ra")
        
    def handle_assign_node(self, node):
        # Allocate space on the stack for the variable
        self.allocate_stack(node.var.name)
        self.process_ast(node.expr)
        stack_offset = self.get_stack_offset(node.var.name)
        self.code.append(f"sw $v0, {stack_offset}($sp)")
        
    def handle_binaryop_node(self, node):
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
    
    def handle_number_node(self, node):
        self.code.append(f"li $v0, {node.value}")
    
    def handle_identifier_node(self, node):
        stack_offset = self.get_stack_offset(node.name)
        self.code.append(f"lw $v0, {stack_offset}($sp)")
        
    def handle_print_node(self, node):
        self.process_ast(node.expr)
        self.code.append("move $a0, $v0")
        self.code.append("li $v0, 1")
        self.code.append("syscall")
        
    def handle_if_node(self, node):
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
            
    def handle_while_node(self, node):
        start_label = self.generate_label("start")
        end_label = self.generate_label("end")
        self.code.append(f"{start_label}:")
        self.process_ast(node.condition)
        self.code.append(f"beq $v0, $zero, {end_label}")
        for stmt in node.body:
            self.process_ast(stmt)
        self.code.append(f"j {start_label}")
        self.code.append(f"{end_label}:")
    
    def handle_dict_node(self, node):
        if node.name not in self.dictionary_map:
            label = f"딕셔너리_{node.name}"
            self.dictionary_map[node.name] = label
            self.data_section.append(f"{label}: .space 400'")
    
    def handle_dict_assign_node(self, node):
        dict_label = self.dictionary_map[node.dict.name]
        self.process_ast(node.key)
        self.code.append(f"sll $t0, $v0, 2")
        self.code.append(f"la $t1, {dict_label}")
        self.code.append(f"add $t2, $t0, $t1")

        # Compute the value to store
        self.process_ast(node.value)
        self.code.append(f"sw $v0, 0($t2)")

    def handle_error_node(self, node):
        self.code.append(f"# Error encountered: {node.message}")
        return False

    def process_ast(self, node):
        if isinstance(node, ast_node.FuncDefNode):
            self.handle_func_def_node(node)
        elif isinstance(node, ast_node.AssignNode):
            self.handle_assign_node(node)
        elif isinstance(node, ast_node.BinaryOpNode):
            self.handle_binaryop_node(node)
        elif isinstance(node, ast_node.NumberNode):
            self.handle_number_node(node)
        elif isinstance(node, ast_node.IdentifierNode):
            self.handle_identifier_node(node)
        elif isinstance(node, ast_node.PrintNode):
            self.handle_print_node(node)
        elif isinstance(node, ast_node.IfNode):
            self.handle_if_node(node)  
        elif isinstance(node, ast_node.WhileNode):
            self.handle_while_node(node)
        elif isinstance(node, ast_node.DictNode):
            self.handle_dict_node(node)
        elif isinstance(node, ast_node.DictAssignNode):
            self.handle_dict_assign_node(node)
        elif isinstance(node, ast_node.ErrorNode):
            self.handle_error_node(node)

    def get_code(self):
        # Combine .data and .text sections
        data_section = "\n".join(self.data_section)
        text_section_lines = []
        for line in self.code:
            text_section_lines.append(line)
            if "# Error encountered" in line:
                break
        text_section = "\n".join(text_section_lines)
        return f".data\n{data_section}\n\n.text\n.globl main\n{text_section}"

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

        output_dir = os.path.dirname(self.output_filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

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
