#!/usr/bin/env python3
"""Entry point for the JAR interpreter."""

import sys
import os
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jar.lexer import Lexer
from jar.parser import Parser
from jar.interpreter import Interpreter


def list_jar_files(directory):
    """List all .jar files in a directory."""
    try:
        jar_files = list(Path(directory).glob("*.jar"))
        if jar_files:
            return [f.name for f in jar_files]
    except Exception:
        pass
    return []


def run_file(filename):
    """Run a JAR script from a file."""
    file_path = Path(filename)
    
    try:
        with open(file_path, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        cwd = os.getcwd()
        print(f"\n❌ Error: File '{filename}' not found.")
        print(f"\n📍 Current working directory:\n   {cwd}")
        
        # List available .jar files
        jar_files = list_jar_files(cwd)
        if jar_files:
            print(f"\n📂 Available .jar files in current directory:")
            for jar_file in jar_files:
                print(f"   - {jar_file}")
        else:
            print(f"\n📂 No .jar files found in current directory")
        
        # Suggest the correct command
        print(f"\n💡 Tip: Make sure the file exists and use the correct path:")
        print(f"   python jar/main.py ./path/to/{os.path.basename(filename)}")
        print()
        sys.exit(1)
    except IOError as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    run_source(source, filename)


def run_source(source, filename="<input>"):
    """Run JAR source code."""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.execute(ast)
    except SyntaxError as e:
        print(f"\n❌ Syntax Error in {filename}:")
        print(f"   {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Runtime Error in {filename}:")
        print(f"   {e}\n", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        cwd = os.getcwd()
        print("🚀 JAR Programming Language Interpreter")
        print(f"\nUsage: python jar/main.py <script.jar>")
        print(f"\nCurrent working directory: {cwd}")
        
        # List available .jar files
        jar_files = list_jar_files(cwd)
        if jar_files:
            print(f"\nAvailable .jar files:")
            for jar_file in jar_files:
                print(f"  - {jar_file}")
        
        print(f"\nExamples:")
        print(f"  python jar/main.py examples/hello.jar")
        print(f"  python jar/main.py ./my-script.jar")
        print()
        sys.exit(1)
    
    script_path = sys.argv[1]
    run_file(script_path)


if __name__ == '__main__':
    main()
