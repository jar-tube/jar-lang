# JAR Programming Language

A simple, expressive programming language with a Python-based interpreter.

## Overview

JAR is a dynamically-typed scripting language designed to be:
- **Simple**: Clean, intuitive syntax inspired by Python and JavaScript
- **Interpreted**: Direct execution via Python runtime
- **Extensible**: Easy to add new features and built-in functions
- **Interactive**: Use it as a REPL or run scripts from files

## Language Features

- Variables and basic types (numbers, strings, booleans, null)
- Arithmetic and logical operations
- Control flow (if/else, while, for)
- Functions with parameters, return values, and recursion
- Lists and dictionaries/objects
- String concatenation with automatic type conversion
- Comments (// style)
- Rich set of built-in functions
- Proper scope management and closures

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
git clone https://github.com/jar-tube/jar-lang.git
cd jar-lang
```

### Running JAR Code

#### Interactive Mode (REPL)
Start an interactive session in your terminal:

```bash
python jar/main.py
```

Then type JAR code directly:
```
🚀 JAR Interactive Interpreter
Type 'exit' to quit, 'help' for commands

jar> let x = 10;
jar> print(x + 5);
15
jar> fn add(a, b) { return a + b; }
jar> print(add(3, 4));
7
jar> exit
Goodbye!
```

#### From a File
Run a JAR script file:

```bash
python jar/main.py script.jar
```

Or run one of the examples:
```bash
python jar/main.py examples/hello.jar
python jar/main.py examples/fibonacci.jar
python jar/main.py examples/loop.jar
python jar/main.py examples/arrays.jar
```

## Examples

### Hello World
```jar
print("Hello, World!");
```

### Variables and Functions
```jar
fn greet(name) {
  print("Hello, " + name + "!");
}

greet("World");
```

### Fibonacci Sequence
```jar
fn fibonacci(n) {
  if (n <= 1) {
    return n;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}

let result = fibonacci(10);
print("fibonacci(10) = " + result);
```

### Loops
```jar
// For loop
for (let i = 0; i < 5; i = i + 1) {
  print("i = " + i);
}

// While loop
let j = 0;
while (j < 3) {
  print("j = " + j);
  j = j + 1;
}
```

### Collections
```jar
// Arrays/Lists
let arr = [1, 2, 3, 4, 5];
print("Array: " + arr);
print("Length: " + len(arr));
print("First element: " + arr[0]);

// Objects/Dictionaries
let obj = {"name": "Alice", "age": 30, "city": "NYC"};
print("Name: " + obj["name"]);
```

## Built-in Functions

### Type Conversion
- `str(value)` - Convert to string
- `num(value)` - Convert to number
- `int(value)` - Convert to integer
- `bool(value)` - Convert to boolean
- `type(value)` - Get the type of a value

### I/O
- `print(*args)` - Print values to console
- `input(prompt)` - Read input from user

### Collections
- `len(obj)` - Get length of a string, list, or dictionary
- `list(*args)` - Create a list from arguments
- `range(start, end, step)` - Create a range of numbers
- `push(list, *values)` - Add values to end of list
- `pop(list, index)` - Remove and return element from list
- `join(list, separator)` - Join list elements into a string
- `split(string, separator)` - Split string into list

## Project Structure

```
jar-lang/
├── jar/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Entry point (REPL + file runner)
│   ├── lexer.py             # Tokenization
│   ├── parser.py            # AST construction
│   ├── interpreter.py       # Execution engine
│   └── builtins.py          # Built-in functions
├── examples/                # Example JAR scripts
│   ├── hello.jar            # Hello World example
│   ├── fibonacci.jar        # Recursive fibonacci
│   ├── loop.jar             # Loop examples
│   └── arrays.jar           # Array/object examples
├── tests/                   # Test suite
│   ├── test_lexer.py        # Lexer tests
│   └── test_interpreter.py  # Interpreter tests
├── README.md                # This file
├── pyproject.toml           # Project configuration
└── .gitignore               # Git ignore rules
```

## Development

### Run Tests
```bash
python -m pytest tests/
```

### Project Architecture

**Lexer** (`jar/lexer.py`) - Tokenizes source code
- Converts raw text into tokens
- Handles strings, numbers, keywords, operators

**Parser** (`jar/parser.py`) - Builds Abstract Syntax Tree (AST)
- Recursive descent parser with proper operator precedence
- Creates a tree representation of the program

**Interpreter** (`jar/interpreter.py`) - Executes the AST
- Tree-walking interpreter
- Manages scopes and variable bindings
- Handles control flow and function calls

**Built-ins** (`jar/builtins.py`) - Standard library functions
- Type conversion functions
- I/O functions
- Collection manipulation

## Syntax Guide

### Variables
```jar
let x = 10;           // Mutable variable
const y = 20;         // Constant variable
```

### Control Flow
```jar
if (condition) {
  // ...
} else {
  // ...
}

while (condition) {
  // ...
}

for (let i = 0; i < 10; i = i + 1) {
  // ...
}
```

### Functions
```jar
fn name(param1, param2) {
  let result = param1 + param2;
  return result;
}
```

### Collections
```jar
let list = [1, 2, 3];
let obj = {"key": "value"};

list[0];        // Access by index
obj["key"];     // Access by key
```

### Comments
```jar
// This is a comment
let x = 5;  // Inline comment
```

## License

MIT License

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
