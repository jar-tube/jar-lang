"""Tests for the interpreter."""

import pytest
from jar.lexer import Lexer
from jar.parser import Parser
from jar.interpreter import Interpreter


def execute(source):
    """Helper to execute JAR code."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    return interpreter.execute(ast)


def test_literals():
    """Test literal values."""
    assert execute("42") == 42
    assert execute("3.14") == 3.14
    assert execute('"hello"') == "hello"
    assert execute("true") == True
    assert execute("false") == False
    assert execute("null") == None


def test_arithmetic():
    """Test arithmetic operations."""
    assert execute("2 + 3") == 5
    assert execute("10 - 4") == 6
    assert execute("3 * 7") == 21
    assert execute("15 / 3") == 5
    assert execute("17 % 5") == 2


def test_comparison():
    """Test comparison operations."""
    assert execute("5 > 3") == True
    assert execute("5 < 3") == False
    assert execute("5 >= 5") == True
    assert execute("5 <= 5") == True
    assert execute("5 == 5") == True
    assert execute("5 != 3") == True


def test_logical():
    """Test logical operations."""
    assert execute("true && true") == True
    assert execute("true && false") == False
    assert execute("true || false") == True
    assert execute("!true") == False
    assert execute("!false") == True


def test_variables():
    """Test variable declaration and usage."""
    assert execute("let x = 42; x") == 42
    assert execute("let x = 10; let y = 20; x + y") == 30


def test_if_statement():
    """Test if statements."""
    source = """let x = 5;
if (x > 3) {
  x = 10;
}
x"""
    assert execute(source) == 10


def test_while_loop():
    """Test while loops."""
    source = """let x = 0;
while (x < 5) {
  x = x + 1;
}
x"""
    assert execute(source) == 5


def test_for_loop():
    """Test for loops."""
    source = """let sum = 0;
for (let i = 0; i < 5; i = i + 1) {
  sum = sum + i;
}
sum"""
    assert execute(source) == 10  # 0 + 1 + 2 + 3 + 4


def test_function():
    """Test function declaration and calls."""
    source = """fn add(a, b) {
  return a + b;
}
add(3, 4)"""
    assert execute(source) == 7


def test_recursion():
    """Test recursive functions."""
    source = """fn fib(n) {
  if (n <= 1) {
    return n;
  }
  return fib(n - 1) + fib(n - 2);
}
fib(6)"""
    assert execute(source) == 8  # Fibonacci(6) = 8


def test_list():
    """Test list operations."""
    assert execute("[1, 2, 3]") == [1, 2, 3]
    assert execute("let arr = [1, 2, 3]; arr[0]") == 1
    assert execute("let arr = [1, 2, 3]; len(arr)") == 3


def test_dict():
    """Test dictionary operations."""
    assert execute('{"a": 1, "b": 2}') == {"a": 1, "b": 2}
    assert execute('let d = {"x": 10}; d["x"]') == 10
