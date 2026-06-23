# JAR Programming Language

A simple, expressive programming language with a Python-based interpreter.

## Overview

JAR is a dynamically-typed scripting language designed to be:
- **Simple**: Clean, intuitive syntax inspired by Python and JavaScript
- **Interpreted**: Direct execution via Python runtime
- **Extensible**: Easy to add new features and built-in functions

## Language Features

- Variables and basic types (numbers, strings, booleans, null)
- Arithmetic and logical operations
- Control flow (if/else, while, for)
- Functions with parameters and return values
- Lists and dictionaries/objects
- Comments
- Built-in functions

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
git clone https://github.com/jar-tube/jar-lang.git
cd jar-lang
```

### Running JAR Code

```bash
python jar/main.py script.jar
```

## Example

```jar
fn greet(name) {
  print("Hello, " + name + "!");
}

greet("World");

let x = 10;
if (x > 5) {
  print("x is greater than 5");
}
```

## Project Structure

```
jar-lang/
├── jar/
│   ├── main.py           # Entry point
│   ├── lexer.py          # Tokenization
│   ├── parser.py         # AST construction
│   ├── interpreter.py    # Execution engine
│   └── builtins.py       # Built-in functions
├── examples/             # Example JAR scripts
├── tests/                # Test suite
└── README.md             # This file
```

## Development

Run tests:
```bash
python -m pytest tests/
```
