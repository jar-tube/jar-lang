#!/usr/bin/env python3
"""Entry point for the JAR interpreter."""

import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jar.lexer import Lexer
from jar.parser import Parser
from jar.interpreter import Interpreter


def run_file(filename):
    """Run a JAR script from a file."""
    try:
        with open(filename, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    run_source(source)


def run_source(source):
    """Run JAR source code."""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.execute(ast)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python jar/main.py <script.jar>")
        sys.exit(1)
    
    script_path = sys.argv[1]
    run_file(script_path)


if __name__ == '__main__':
    main()
