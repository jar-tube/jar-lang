#!/usr/bin/env python3
"""Entry point for the JAR interpreter."""

import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jar.lexer import Lexer
from jar.parser import Parser
from jar.interpreter import Interpreter


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
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def run_interactive():
    """Run interactive REPL mode."""
    print("🚀 JAR Interactive Interpreter")
    print("Type 'exit' to quit, 'help' for commands\n")
    
    interpreter = Interpreter()
    
    while True:
        try:
            # Read input
            user_input = input("jar> ").strip()
            
            # Handle special commands
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("""
Available commands:
  exit          - Exit the interpreter
  help          - Show this help message
  
Examples:
  let x = 10;
  print(x + 5);
  fn add(a, b) { return a + b; }
  print(add(3, 4));
""")
                continue
            
            # Parse and execute
            try:
                lexer = Lexer(user_input)
                tokens = lexer.tokenize()
                
                parser = Parser(tokens)
                ast = parser.parse()
                
                # Execute each statement
                for stmt in ast.statements:
                    result = interpreter.execute(stmt)
                    # Print non-None results
                    if result is not None and not isinstance(result, type(None)):
                        # Format output nicely
                        if isinstance(result, bool):
                            print(result)
                        elif isinstance(result, float) and result.is_integer():
                            print(int(result))
                        else:
                            print(result)
            except SyntaxError as e:
                print(f"Syntax Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


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

    run_source(source, filename)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # No arguments - start interactive mode
        run_interactive()
    else:
        # File argument provided
        script_path = sys.argv[1]
        run_file(script_path)


if __name__ == '__main__':
    main()
