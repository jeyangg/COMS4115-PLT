import re
import os
import sys

import lexer_2
import ast_node
from parser import Parser
from codegen import MIPSCodeGenerator

class OptimizingMIPSCodeGenerator(MIPSCodeGenerator):
    def __init__(self):
        super().__init__()
        self.constant_map = {}  # For constant propagation

    def optimize_ast(self, node):
        """Optimize the AST before code generation."""
        if isinstance(node, ast_node.BinaryOpNode):
            # Constant Folding
            if isinstance(node.left, ast_node.NumberNode) and isinstance(node.right, ast_node.NumberNode):
                result = self.fold_constants(node.operator, node.left.value, node.right.value)
                return ast_node.NumberNode(result)

            # Recursively optimize left and right subtrees
            node.left = self.optimize_ast(node.left)
            node.right = self.optimize_ast(node.right)

            # Algebraic Simplifications
            if self.is_identity_operation(node):
                return node.left if node.right.value == 0 else node.right

        elif isinstance(node, ast_node.AssignNode):
            # Constant Propagation
            optimized_expr = self.optimize_ast(node.expr)
            if isinstance(optimized_expr, ast_node.NumberNode):
                self.constant_map[node.var.name] = optimized_expr.value
            return ast_node.AssignNode(node.var, optimized_expr)

        elif isinstance(node, ast_node.IdentifierNode):
            # Replace variable with constant if available
            if node.name in self.constant_map:
                return ast_node.NumberNode(self.constant_map[node.name])

        elif isinstance(node, ast_node.WhileNode):
            # Dead Code Elimination
            condition = self.optimize_ast(node.condition)
            if isinstance(condition, ast_node.BooleanNode) and not condition.value:
                return None  # Remove the entire loop
            node.condition = condition
            node.body = [self.optimize_ast(stmt) for stmt in node.body if stmt]
            return node

        elif isinstance(node, ast_node.IfNode):
            condition = self.optimize_ast(node.condition)
            # Dead Code Elimination for Always True/False Conditions
            if isinstance(condition, ast_node.BooleanNode):
                if condition.value:
                    return [self.optimize_ast(stmt) for stmt in node.body]
                else:
                    return [self.optimize_ast(stmt) for stmt in node.else_body] if node.else_body else None
            node.condition = condition
            node.body = [self.optimize_ast(stmt) for stmt in node.body if stmt]
            node.else_body = [self.optimize_ast(stmt) for stmt in node.else_body if stmt] if node.else_body else None
            return node

        return node

    def fold_constants(self, operator, left, right):
        """Perform constant folding."""
        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            return left // right if right != 0 else 0  # Avoid division by zero
        elif operator == "==":
            return int(left == right)
        elif operator == "!=":
            return int(left != right)
        elif operator == "<":
            return int(left < right)
        elif operator == ">":
            return int(left > right)
        elif operator == "<=":
            return int(left <= right)
        elif operator == ">=":
            return int(left >= right)
        return None

    def is_identity_operation(self, node):
        """Check for algebraic simplifications like x + 0 or x * 1."""
        if node.operator == "+" and isinstance(node.right, ast_node.NumberNode) and node.right.value == 0:
            return True
        if node.operator == "*" and isinstance(node.right, ast_node.NumberNode) and node.right.value == 1:
            return True
        return False

    def process_ast(self, node):
        """Override the process_ast method to include optimizations."""
        optimized_node = self.optimize_ast(node)
        if optimized_node:
            super().process_ast(optimized_node)


class OptimizedPipeline:
    def __init__(self, source_code, output_filename):
        self.generator = OptimizingMIPSCodeGenerator()
        self.source_code = source_code
        self.output_filename = output_filename

    def process(self):
        # Step 1: Lexical Analysis
        parser = Parser(self.source_code)
        ast = parser.parse()

        # Step 2: Perform Optimizations
        optimized_ast = [self.generator.optimize_ast(node) for node in ast if node]

        # Step 3: Code Generation
        for node in optimized_ast:
            self.generator.process_ast(node)

        # Step 4: Output the generated code
        generated_code = self.generator.get_code()
        output_dir = os.path.dirname(self.output_filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
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

    pipeline = OptimizedPipeline(source_code, output_filename)
    pipeline.process()
