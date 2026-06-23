"""Lexer for JAR language - tokenizes source code."""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Token types for JAR language."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNCTION = auto()
    RETURN = auto()
    LET = auto()
    CONST = auto()
    BREAK = auto()
    CONTINUE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()           # ==
    NE = auto()           # !=
    LT = auto()           # <
    LE = auto()           # <=
    GT = auto()           # >
    GE = auto()           # >=
    ASSIGN = auto()       # =
    PLUS_ASSIGN = auto()  # +=
    MINUS_ASSIGN = auto() # -=
    AND = auto()          # &&
    OR = auto()           # ||
    NOT = auto()          # !
    BITWISE_AND = auto()  # &
    BITWISE_OR = auto()   # |
    BITWISE_XOR = auto()  # ^
    BITWISE_NOT = auto()  # ~
    LSHIFT = auto()       # <<
    RSHIFT = auto()       # >>
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    ARROW = auto()        # =>
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a single token."""
    type: TokenType
    value: any
    line: int
    column: int


class Lexer:
    """Tokenizes JAR source code."""
    
    KEYWORDS = {
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'fn': TokenType.FUNCTION,
        'function': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'let': TokenType.LET,
        'const': TokenType.CONST,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NULL,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        """Raise a lexer error."""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Peek at a character without consuming it."""
        pos = self.position + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return the next character."""
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        """Skip whitespace (but not newlines)."""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments."""
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_string(self, quote: str) -> str:
        """Read a string literal."""
        result = ''
        self.advance()  # Skip opening quote
        
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    result += '\n'
                elif next_char == 't':
                    result += '\t'
                elif next_char == 'r':
                    result += '\r'
                elif next_char == '\\':
                    result += '\\'
                elif next_char == quote:
                    result += quote
                else:
                    result += next_char
            else:
                result += self.advance()
        
        if not self.peek():
            self.error(f"Unterminated string")
        
        self.advance()  # Skip closing quote
        return result
    
    def read_number(self) -> float:
        """Read a number literal."""
        result = ''
        has_dot = False
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            result += self.advance()
        
        return float(result) if has_dot else int(result)
    
    def read_identifier(self) -> str:
        """Read an identifier or keyword."""
        result = ''
        while self.peek() and (self.peek().isalnum() or self.peek() in '_$'):
            result += self.advance()
        return result
    
    def add_token(self, token_type: TokenType, value: any = None):
        """Add a token to the tokens list."""
        token = Token(token_type, value, self.line, self.column)
        self.tokens.append(token)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code and return a list of tokens."""
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.peek() is None:
                break
            
            # Comments
            if self.peek() == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            # Newlines
            if self.peek() == '\n':
                self.advance()
                continue
            
            # Strings
            if self.peek() in '"\'':
                quote = self.peek()
                string_val = self.read_string(quote)
                self.add_token(TokenType.STRING, string_val)
                continue
            
            # Numbers
            if self.peek().isdigit():
                num_val = self.read_number()
                self.add_token(TokenType.NUMBER, num_val)
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() in '_$':
                identifier = self.read_identifier()
                token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                value = identifier if token_type == TokenType.IDENTIFIER else None
                self.add_token(token_type, value)
                continue
            
            # Operators and delimiters
            char = self.peek()
            next_char = self.peek(1)
            
            # Two-character operators
            two_char = char + (next_char or '')
            two_char_ops = {
                '==': TokenType.EQ,
                '!=': TokenType.NE,
                '<=': TokenType.LE,
                '>=': TokenType.GE,
                '&&': TokenType.AND,
                '||': TokenType.OR,
                '+=': TokenType.PLUS_ASSIGN,
                '-=': TokenType.MINUS_ASSIGN,
                '=>': TokenType.ARROW,
                '<<': TokenType.LSHIFT,
                '>>': TokenType.RSHIFT,
            }
            
            if two_char in two_char_ops:
                self.add_token(two_char_ops[two_char])
                self.advance()
                self.advance()
                continue
            
            # Single-character tokens
            single_char_ops = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '%': TokenType.PERCENT,
                '=': TokenType.ASSIGN,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '!': TokenType.NOT,
                '&': TokenType.BITWISE_AND,
                '|': TokenType.BITWISE_OR,
                '^': TokenType.BITWISE_XOR,
                '~': TokenType.BITWISE_NOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
            }
            
            if char in single_char_ops:
                self.add_token(single_char_ops[char])
                self.advance()
                continue
            
            self.error(f"Unexpected character: '{char}'")
        
        self.add_token(TokenType.EOF)
        return self.tokens
