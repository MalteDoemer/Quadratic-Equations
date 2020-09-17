from Lexer import Lexer, Token, TokenKind

CONSTANT_TOKENS = [
    TokenKind.Number,
    TokenKind.Imaginary
]

UNARY_TOKENS = [
    TokenKind.Plus,
    TokenKind.Minus
]

SUM_TOKENS = [
    TokenKind.Plus,
    TokenKind.Minus
]

PRODUCT_TOKENS = [
    TokenKind.Star,
    TokenKind.Slash,
    TokenKind.Imaginary,
    TokenKind.LParen
]

IMPLICIT_MULTIPLY = [
    TokenKind.Imaginary,
    TokenKind.LParen
]


class Expression:
    def __repr__(self):
        return str(self)

    def eval(self):
        raise NotImplementedError


class BinaryOperation(Expression):
    def __init__(self, operator: str, left: Expression, right: Expression):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

    def eval(self):
        if self.operator == '+':
            return self.left.eval() + self.right.eval()
        elif self.operator == '-':
            return self.left.eval() - self.right.eval()
        elif self.operator == '*':
            return self.left.eval() * self.right.eval()
        elif self.operator == '/':
            return self.left.eval() / self.right.eval()
        else:
            return NotImplemented


class UnaryOperation(Expression):
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"({self.operator}{self.operand})"

    def eval(self):
        if self.operator == '+':
            return self.operand.eval()
        elif self.operator == '-':
            return - self.operand.eval()
        else:
            return NotImplemented


class Constant(Expression):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)

    def eval(self):
        return self.num


class Invalid(Expression):
    def __str__(self):
        return f"NaN"

    def eval(self):
        return NotImplemented


class Parser:
    def __init__(self, term: str, errors: list):
        self.lexer = iter(Lexer(term))
        self.current: Token = next(self.lexer)
        self.errors = errors

    def advance(self):
        hold = self.current
        if hold.kind != TokenKind.End:
            self.current = next(self.lexer)
        return hold

    def match(self, kind: TokenKind):
        if self.current.kind != kind:
            self.errors.append(f"Unexpected Token: '{self.current.value}'")
            tok = Token(kind, self.current.value)
            self.advance()
            return tok
        else:
            return self.advance()

    def parse(self):
        hold = self.parse_sum()
        self.match(TokenKind.End)
        return hold

    def parse_sum(self):
        left = self.parse_product()
        while self.current.kind in SUM_TOKENS:
            op = self.advance().value
            right = self.parse_product()
            left = BinaryOperation(op, left, right)
        return left

    def parse_product(self):
        left = self.parse_primary()
        while self.current.kind in PRODUCT_TOKENS:
            op = "*" if self.current.kind in IMPLICIT_MULTIPLY else self.advance().value
            right = self.parse_primary()
            left = BinaryOperation(op, left, right)
        return left

    def parse_primary(self):
        if self.current.kind in CONSTANT_TOKENS:
            return Constant(self.advance().value)
        elif self.current.kind in UNARY_TOKENS:
            op = self.advance()
            expr = self.parse_primary()
            return UnaryOperation(op.value, expr)
        elif self.current.kind == TokenKind.LParen:
            self.advance()
            expr = self.parse_sum()
            self.match(TokenKind.RParen)
            return expr
        elif self.current.kind == TokenKind.Bad:
            self.errors.append(f"Bad Token: '{self.current.value}'")
            self.advance()
            return Invalid()
        else:
            self.errors.append(f"Unexpected Token: '{self.current.kind}'")
            self.advance()
            return Invalid()
