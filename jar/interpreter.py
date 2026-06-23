"""Interpreter for JAR language - executes AST."""

from typing import Any, Dict, List, Optional, Callable
from jar.parser import *
from jar.builtins import get_builtin_functions


class BreakException(Exception):
    """Exception for break statement."""
    pass


class ContinueException(Exception):
    """Exception for continue statement."""
    pass


class ReturnException(Exception):
    """Exception for return statement."""
    def __init__(self, value):
        self.value = value


class JARFunction:
    """Represents a user-defined function."""
    def __init__(self, parameters: List[str], body: List[ASTNode], closure: Dict[str, Any]):
        self.parameters = parameters
        self.body = body
        self.closure = closure


class Interpreter:
    """Executes JAR AST."""
    
    def __init__(self):
        self.global_scope = get_builtin_functions()
        self.scopes: List[Dict[str, Any]] = [self.global_scope]
    
    def current_scope(self) -> Dict[str, Any]:
        """Get the current scope."""
        return self.scopes[-1]
    
    def push_scope(self):
        """Push a new scope."""
        self.scopes.append({})
    
    def pop_scope(self):
        """Pop the current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def define(self, name: str, value: Any):
        """Define a variable in the current scope."""
        self.current_scope()[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable value, searching from innermost to outermost scope."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Undefined variable: '{name}'")
    
    def set(self, name: str, value: Any):
        """Set a variable value, searching from innermost to outermost scope."""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise NameError(f"Undefined variable: '{name}'")
    
    def execute(self, node: ASTNode) -> Any:
        """Execute an AST node."""
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.execute(stmt)
            return result
        
        elif isinstance(node, NumberLiteral):
            return node.value
        
        elif isinstance(node, StringLiteral):
            return node.value
        
        elif isinstance(node, BooleanLiteral):
            return node.value
        
        elif isinstance(node, NullLiteral):
            return None
        
        elif isinstance(node, Identifier):
            return self.get(node.name)
        
        elif isinstance(node, ListLiteral):
            return [self.execute(elem) for elem in node.elements]
        
        elif isinstance(node, DictLiteral):
            result = {}
            for key_expr, value_expr in node.pairs:
                key = self.execute(key_expr)
                value = self.execute(value_expr)
                result[key] = value
            return result
        
        elif isinstance(node, BinaryOp):
            return self.execute_binary_op(node)
        
        elif isinstance(node, UnaryOp):
            return self.execute_unary_op(node)
        
        elif isinstance(node, Assignment):
            value = self.execute(node.value)
            self.set(node.target, value)
            return value
        
        elif isinstance(node, VariableDeclaration):
            value = None if node.value is None else self.execute(node.value)
            self.define(node.name, value)
            return None
        
        elif isinstance(node, FunctionDeclaration):
            func = JARFunction(node.parameters, node.body, self.current_scope().copy())
            self.define(node.name, func)
            return None
        
        elif isinstance(node, FunctionCall):
            return self.execute_function_call(node)
        
        elif isinstance(node, IfStatement):
            condition = self.execute(node.condition)
            if self.is_truthy(condition):
                result = None
                for stmt in node.then_branch:
                    result = self.execute(stmt)
                return result
            elif node.else_branch:
                result = None
                for stmt in node.else_branch:
                    result = self.execute(stmt)
                return result
            return None
        
        elif isinstance(node, WhileStatement):
            result = None
            while self.is_truthy(self.execute(node.condition)):
                try:
                    for stmt in node.body:
                        result = self.execute(stmt)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return result
        
        elif isinstance(node, ForStatement):
            result = None
            self.push_scope()
            try:
                if node.init:
                    self.execute(node.init)
                
                while True:
                    if node.condition and not self.is_truthy(self.execute(node.condition)):
                        break
                    
                    try:
                        for stmt in node.body:
                            result = self.execute(stmt)
                    except BreakException:
                        break
                    except ContinueException:
                        pass
                    
                    if node.increment:
                        self.execute(node.increment)
            finally:
                self.pop_scope()
            return result
        
        elif isinstance(node, ReturnStatement):
            value = None if node.value is None else self.execute(node.value)
            raise ReturnException(value)
        
        elif isinstance(node, BreakStatement):
            raise BreakException()
        
        elif isinstance(node, ContinueStatement):
            raise ContinueException()
        
        elif isinstance(node, IndexAccess):
            obj = self.execute(node.object)
            index = self.execute(node.index)
            try:
                return obj[index]
            except (KeyError, IndexError, TypeError) as e:
                raise TypeError(f"Cannot index {type(obj).__name__} with {type(index).__name__}")
        
        elif isinstance(node, MemberAccess):
            obj = self.execute(node.object)
            if isinstance(obj, dict) and node.member in obj:
                return obj[node.member]
            raise AttributeError(f"'{type(obj).__name__}' has no attribute '{node.member}'")
        
        else:
            raise RuntimeError(f"Unknown node type: {type(node).__name__}")
    
    def execute_binary_op(self, node: BinaryOp) -> Any:
        """Execute a binary operation."""
        left = self.execute(node.left)
        right = self.execute(node.right)
        
        if node.operator == TokenType.PLUS:
            return left + right
        elif node.operator == TokenType.MINUS:
            return left - right
        elif node.operator == TokenType.STAR:
            return left * right
        elif node.operator == TokenType.SLASH:
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif node.operator == TokenType.PERCENT:
            return left % right
        elif node.operator == TokenType.EQ:
            return left == right
        elif node.operator == TokenType.NE:
            return left != right
        elif node.operator == TokenType.LT:
            return left < right
        elif node.operator == TokenType.LE:
            return left <= right
        elif node.operator == TokenType.GT:
            return left > right
        elif node.operator == TokenType.GE:
            return left >= right
        elif node.operator == TokenType.AND:
            return self.is_truthy(left) and self.is_truthy(right)
        elif node.operator == TokenType.OR:
            return left if self.is_truthy(left) else right
        elif node.operator == TokenType.BITWISE_AND:
            return int(left) & int(right)
        elif node.operator == TokenType.BITWISE_OR:
            return int(left) | int(right)
        elif node.operator == TokenType.BITWISE_XOR:
            return int(left) ^ int(right)
        elif node.operator == TokenType.LSHIFT:
            return int(left) << int(right)
        elif node.operator == TokenType.RSHIFT:
            return int(left) >> int(right)
        else:
            raise RuntimeError(f"Unknown binary operator: {node.operator}")
    
    def execute_unary_op(self, node: UnaryOp) -> Any:
        """Execute a unary operation."""
        operand = self.execute(node.operand)
        
        if node.operator == TokenType.NOT:
            return not self.is_truthy(operand)
        elif node.operator == TokenType.MINUS:
            return -operand
        elif node.operator == TokenType.PLUS:
            return +operand
        elif node.operator == TokenType.BITWISE_NOT:
            return ~int(operand)
        else:
            raise RuntimeError(f"Unknown unary operator: {node.operator}")
    
    def execute_function_call(self, node: FunctionCall) -> Any:
        """Execute a function call."""
        callee = self.execute(node.callee)
        args = [self.execute(arg) for arg in node.arguments]
        
        # Built-in function
        if callable(callee) and not isinstance(callee, JARFunction):
            return callee(*args)
        
        # User-defined function
        if isinstance(callee, JARFunction):
            if len(args) != len(callee.parameters):
                raise TypeError(f"Expected {len(callee.parameters)} arguments, got {len(args)}")
            
            # Create new scope for function execution
            self.push_scope()
            try:
                # Bind parameters
                for param, arg in zip(callee.parameters, args):
                    self.define(param, arg)
                
                # Execute function body
                result = None
                for stmt in callee.body:
                    result = self.execute(stmt)
                return result
            except ReturnException as e:
                return e.value
            finally:
                self.pop_scope()
        
        raise TypeError(f"'{callee}' is not callable")
    
    @staticmethod
    def is_truthy(value: Any) -> bool:
        """Determine if a value is truthy in JAR."""
        if value is None or value is False:
            return False
        if value == 0 or value == "" or value == [] or value == {}:
            return False
        return True
