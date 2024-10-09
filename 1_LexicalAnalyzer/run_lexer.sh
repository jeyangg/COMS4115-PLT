#!/bin/bash

# Ensure Python 3.5 or above is installed
if ! command -v python3.5 &> /dev/null
then
    echo "Python 3.5 is not installed. Please install Python 3.5."
    exit 1
fi

# Run lexer on each sample program in the samples folder
for file in samples/*.txt
do
    echo "Running lexer on $file"
    python3.5 lexer.py "$file"
    echo "------------------------------------"
done