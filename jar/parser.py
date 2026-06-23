"""Parser for JAR language - builds AST from tokens."""

from dataclasses import dataclass
from typing import List, Optional, Any
from jar.lexer import Token, TokenType


# AST Node Types
@dataclass
class ASTNode:
    """Base class for AST nodes."""
    pass


@dataclass
class Program(ASTNode):
    """Root node of the AST."""
    statements: List[ASTNode]


@dataclass
class NumberLiteral(ASTNode):
    """Numeric literal."""
    value: float


@dataclass
class StringLiteral(ASTNode):
    """String literal."""
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    """Boolean literal."""
    value: bool


@dataclass
class NullLiteral(ASTNode):
    """Null literal."""
    pass


@dataclass
class Identifier(ASTNode):
    """Variable identifier."""
    name: str


@dataclass
class BinaryOp(ASTNode):
    """Binary operation."""
    left: ASTNode
    operator: TokenType
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """Unary operation."""
    operator: TokenType
    operand: ASTNode


@dataclass
class Assignment(ASTNode):
    """Variable assignment."""
    target: str
    value: ASTNode


@dataclass
class VariableDeclaration(ASTNode):
    """Variable declaration."""
    name: str
    value: Optional[ASTNode]
    is_const: bool


@dataclass
class IfStatement(ASTNode):
    """If statement."""
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]]


@dataclass
class WhileStatement(ASTNode):
    """While loop."""
    condition: ASTNode
    body: List[ASTNode]


@dataclass
class ForStatement(ASTNode):
    """For loop."""
    init: Optional[ASTNode]
    condition: Optional[ASTNode]
    increment: Optional[ASTNode]
    body: List[ASTNode]


@dataclass
class FunctionDeclaration(ASTNode):
    """Function declaration."""
    name: str
    parameters: List[str]
    body: List[ASTNode]


@dataclass
class FunctionCall(ASTNode):
    """Function call."""
    callee: ASTNode
    arguments: List[ASTNode]


@dataclass
class ReturnStatement(ASTNode):
    """Return statement."""
    value: Optional[ASTNode]


@dataclass
class BreakStatement(ASTNode):
    """Break statement."""
    pass


@dataclass
class ContinueStatement(ASTNode):
    """Continue statement."""
    pass


@dataclass
class ListLiteral(ASTNode):
    """List/array literal."""
    elements: List[ASTNode]


@dataclass
class DictLiteral(ASTNode):
    """Dictionary/object literal."""
    pairs: List[tuple]  # List of (key, value) tuples


@dataclass
class IndexAccess(ASTNode):
    """Array/dict index access."""
    object: ASTNode
    index: ASTNode


@dataclass
class MemberAccess(ASTNode):
    """Object member access."""
    object: ASTNode
    member: str


class Parser:
    """Parses tokens into an AST."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def error(self, message: str):
        """Raise a parser error."""
        token = self.current_token()
        raise SyntaxError(f"Parser error at line {token.line}, column {token.column}: {message}")
    
    def current_token(self) -> Token:
        """Get the current token."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at a future token."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        """Consume and return the current token."""
        token = self.current_token()
        if token.type != TokenType.EOF:
            self.position += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume a token of the expected type or raise an error."""
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token().type in token_types
    
    def consume_if(self, token_type: TokenType) -> bool:
        """Consume token if it matches the type."""
        if self.match(token_type):
            self.advance()
            return True
        return False
    
    def parse(self) -> Program:
        """Parse the entire program."""
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement."""
        # Variable declaration
        if self.match(TokenType.LET, TokenType.CONST):
            is_const = self.match(TokenType.CONST)
            self.advance()
            return self.parse_variable_declaration(is_const)
        
        # Function declaration
        if self.match(TokenType.FUNCTION):
            self.advance()
            return self.parse_function_declaration()
        
        # If statement
        if self.match(TokenType.IF):
            self.advance()
            return self.parse_if_statement()
        
        # While loop
        if self.match(TokenType.WHILE):
            self.advance()
            return self.parse_while_statement()
        
        # For loop
        if self.match(TokenType.FOR):
            self.advance()
            return self.parse_for_statement()
        
        # Return statement
        if self.match(TokenType.RETURN):
            self.advance()
            return self.parse_return_statement()
        
        # Break statement
        if self.match(TokenType.BREAK):
            self.advance()
            self.consume_if(TokenType.SEMICOLON)
            return BreakStatement()
        
        # Continue statement
        if self.match(TokenType.CONTINUE):
            self.advance()
            self.consume_if(TokenType.SEMICOLON)
            return ContinueStatement()
        
        # Expression statement
        expr = self.parse_expression()
        self.consume_if(TokenType.SEMICOLON)
        return expr
    
    def parse_variable_declaration(self, is_const: bool) -> VariableDeclaration:
        """Parse a variable declaration."""
        name = self.expect(TokenType.IDENTIFIER).value
        
        value = None
        if self.consume_if(TokenType.ASSIGN):
            value = self.parse_expression()
        
        self.consume_if(TokenType.SEMICOLON)
        return VariableDeclaration(name, value, is_const)
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """Parse a function declaration."""
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        parameters = []
        if not self.match(TokenType.RPAREN):
            parameters.append(self.expect(TokenType.IDENTIFIER).value)
            while self.consume_if(TokenType.COMMA):
                parameters.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        
        return FunctionDeclaration(name, parameters, body)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse an if statement."""
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        then_branch = self.parse_block()
        
        else_branch = None
        if self.consume_if(TokenType.ELSE):
            self.expect(TokenType.LBRACE)
            else_branch = self.parse_block()
        
        return IfStatement(condition, then_branch, else_branch)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse a while loop."""
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        """Parse a for loop."""
        self.expect(TokenType.LPAREN)
        
        init = None
        if not self.match(TokenType.SEMICOLON):
            init = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        increment = None
        if not self.match(TokenType.RPAREN):
            increment = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        body = self.parse_block()
        
        return ForStatement(init, condition, increment, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse a return statement."""
        value = None
        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.parse_expression()
        self.consume_if(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_block(self) -> List[ASTNode]:
        """Parse a block of statements."""
        statements = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return statements
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression."""
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        """Parse an assignment or lower-level expression."""
        expr = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            if not isinstance(expr, Identifier):
                self.error("Invalid assignment target")
            self.advance()
            value = self.parse_assignment()
            return Assignment(expr.name, value)
        
        return expr
    
    def parse_logical_or(self) -> ASTNode:
        """Parse logical OR expressions."""
        expr = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op = self.advance().type
            right = self.parse_logical_and()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_logical_and(self) -> ASTNode:
        """Parse logical AND expressions."""
        expr = self.parse_bitwise_or()
        
        while self.match(TokenType.AND):
            op = self.advance().type
            right = self.parse_bitwise_or()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_bitwise_or(self) -> ASTNode:
        """Parse bitwise OR expressions."""
        expr = self.parse_bitwise_xor()
        
        while self.match(TokenType.BITWISE_OR):
            op = self.advance().type
            right = self.parse_bitwise_xor()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_bitwise_xor(self) -> ASTNode:
        """Parse bitwise XOR expressions."""
        expr = self.parse_bitwise_and()
        
        while self.match(TokenType.BITWISE_XOR):
            op = self.advance().type
            right = self.parse_bitwise_and()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_bitwise_and(self) -> ASTNode:
        """Parse bitwise AND expressions."""
        expr = self.parse_equality()
        
        while self.match(TokenType.BITWISE_AND):
            op = self.advance().type
            right = self.parse_equality()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_equality(self) -> ASTNode:
        """Parse equality expressions."""
        expr = self.parse_comparison()
        
        while self.match(TokenType.EQ, TokenType.NE):
            op = self.advance().type
            right = self.parse_comparison()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expressions."""
        expr = self.parse_shift()
        
        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.advance().type
            right = self.parse_shift()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_shift(self) -> ASTNode:
        """Parse bit shift expressions."""
        expr = self.parse_additive()
        
        while self.match(TokenType.LSHIFT, TokenType.RSHIFT):
            op = self.advance().type
            right = self.parse_additive()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_additive(self) -> ASTNode:
        """Parse addition and subtraction."""
        expr = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().type
            right = self.parse_multiplicative()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication, division, and modulo."""
        expr = self.parse_unary()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.advance().type
            right = self.parse_unary()
            expr = BinaryOp(expr, op, right)
        
        return expr
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expressions."""
        if self.match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS, TokenType.BITWISE_NOT):
            op = self.advance().type
            expr = self.parse_unary()
            return UnaryOp(op, expr)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parse postfix expressions (function calls, indexing, member access)."""
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                # Function call
                self.advance()
                arguments = []
                if not self.match(TokenType.RPAREN):
                    arguments.append(self.parse_expression())
                    while self.consume_if(TokenType.COMMA):
                        arguments.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                expr = FunctionCall(expr, arguments)
            elif self.match(TokenType.LBRACKET):
                # Index access
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            elif self.match(TokenType.DOT):
                # Member access
                self.advance()
                member = self.expect(TokenType.IDENTIFIER).value
                expr = MemberAccess(expr, member)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions."""
        # Numbers
        if self.match(TokenType.NUMBER):
            value = self.advance().value
            return NumberLiteral(value)
        
        # Strings
        if self.match(TokenType.STRING):
            value = self.advance().value
            return StringLiteral(value)
        
        # Booleans
        if self.match(TokenType.TRUE):
            self.advance()
            return BooleanLiteral(True)
        
        if self.match(TokenType.FALSE):
            self.advance()
            return BooleanLiteral(False)
        
        # Null
        if self.match(TokenType.NULL):
            self.advance()
            return NullLiteral()
        
        # Identifiers
        if self.match(TokenType.IDENTIFIER):
            name = self.advance().value
            return Identifier(name)
        
        # Lists
        if self.match(TokenType.LBRACKET):
            self.advance()
            elements = []
            if not self.match(TokenType.RBRACKET):
                elements.append(self.parse_expression())
                while self.consume_if(TokenType.COMMA):
                    if self.match(TokenType.RBRACKET):
                        break
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET)
            return ListLiteral(elements)
        
        # Dictionaries
        if self.match(TokenType.LBRACE):
            self.advance()
            pairs = []
            if not self.match(TokenType.RBRACE):
                # Parse key
                key_expr = self.parse_expression()
                self.expect(TokenType.COLON)
                value_expr = self.parse_expression()
                pairs.append((key_expr, value_expr))
                while self.consume_if(TokenType.COMMA):
                    if self.match(TokenType.RBRACE):
                        break
                    key_expr = self.parse_expression()
                    self.expect(TokenType.COLON)
                    value_expr = self.parse_expression()
                    pairs.append((key_expr, value_expr))
            self.expect(TokenType.RBRACE)
            return DictLiteral(pairs)
        
        # Parenthesized expressions
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token: {self.current_token().type}")
