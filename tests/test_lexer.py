"""Tests for the lexer."""

import pytest
from jar.lexer import Lexer, TokenType


def test_number_tokens():
    """Test tokenization of numbers."""
    lexer = Lexer("42 3.14 0")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == 3.14
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == 0


def test_string_tokens():
    """Test tokenization of strings."""
    lexer = Lexer('"hello" \'world\'')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "world"


def test_keywords():
    """Test tokenization of keywords."""
    lexer = Lexer("if else while for fn return let const true false null")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.ELSE
    assert tokens[2].type == TokenType.WHILE
    assert tokens[3].type == TokenType.FOR
    assert tokens[4].type == TokenType.FUNCTION
    assert tokens[5].type == TokenType.RETURN
    assert tokens[6].type == TokenType.LET
    assert tokens[7].type == TokenType.CONST
    assert tokens[8].type == TokenType.TRUE
    assert tokens[9].type == TokenType.FALSE
    assert tokens[10].type == TokenType.NULL


def test_operators():
    """Test tokenization of operators."""
    lexer = Lexer("+ - * / % == != < > <= >= && ||")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.PLUS
    assert tokens[1].type == TokenType.MINUS
    assert tokens[2].type == TokenType.STAR
    assert tokens[3].type == TokenType.SLASH
    assert tokens[4].type == TokenType.PERCENT
    assert tokens[5].type == TokenType.EQ
    assert tokens[6].type == TokenType.NE
    assert tokens[7].type == TokenType.LT
    assert tokens[8].type == TokenType.GT
    assert tokens[9].type == TokenType.LE
    assert tokens[10].type == TokenType.GE
    assert tokens[11].type == TokenType.AND
    assert tokens[12].type == TokenType.OR


def test_delimiters():
    """Test tokenization of delimiters."""
    lexer = Lexer("( ) { } [ ] ; , . :")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.LPAREN
    assert tokens[1].type == TokenType.RPAREN
    assert tokens[2].type == TokenType.LBRACE
    assert tokens[3].type == TokenType.RBRACE
    assert tokens[4].type == TokenType.LBRACKET
    assert tokens[5].type == TokenType.RBRACKET
    assert tokens[6].type == TokenType.SEMICOLON
    assert tokens[7].type == TokenType.COMMA
    assert tokens[8].type == TokenType.DOT
    assert tokens[9].type == TokenType.COLON


def test_comments():
    """Test that comments are ignored."""
    lexer = Lexer("42 // this is a comment\n3.14")
    tokens = lexer.tokenize()
    assert len(tokens) == 3  # 42, 3.14, EOF
    assert tokens[0].value == 42
    assert tokens[1].value == 3.14
