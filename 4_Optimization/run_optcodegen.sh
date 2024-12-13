#!/bin/bash

# Usage message
if [ "$#" -ne 1 ]; then
  echo "Usage: ./run_parser.sh <input_file>"
  exit 1
fi

# Input file with source code
INPUT_FILE=$1

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File '$INPUT_FILE' not found."
  exit 1
fi

# Run the code generator
echo "Running code generator on $INPUT_FILE..."

# Run the code generator
TOKENS=$(python3 optimizer.py "$INPUT_FILE")

# Check if codeg generator ran successfully
if [ $? -ne 0 ]; then
  echo "Optimized code generation failed."
  exit 1
fi

# Print result of AST generation
echo "Optimzied code has been generated."