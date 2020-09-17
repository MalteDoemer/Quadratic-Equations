from enum import Enum
from Mcomplex import Complex


class TokenKind(Enum):
    Bad = -1
    End = 0
    Number = 1
    Imaginary = 2
    Plus = 3
    Minus = 4
    Star = 5
    Slash = 6
    LParen = 7
    RParen = 8


class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return f"{self.kind} : '{self.value}'"

    def __repr__(self):
        return str(self)


class Lexer:
    def __init__(self, term: str):
        self.term = term
        self.pos = -1
        self.current = ''
        self.advance()

    def advance(self):
        hold = self.current
        self.pos += 1
        self.current = self.term[self.pos] if self.pos < len(
            self.term) else '\0'
        return hold

    def lex_number(self):
        num = 0
        while self.current in '0123456789':
            num *= 10
            num += int(self.current)
            self.advance()

        if self.current == '.':
            self.advance()
            if self.current not in '0123456789':
                return Token(TokenKind.Bad, self.advance())

            scale = 1
            while self.current in '0123456789':
                scale *= 10
                num += int(self.current) / scale
                self.advance()

        return Token(TokenKind.Number, num)

    def skip_space(self):
        while self.current.isspace():
            self.advance()
        return self.next_token()

    def next_token(self):
        if self.current.isspace():
            return self.skip_space()
        elif self.current == '\0':
            return Token(TokenKind.End, self.advance())
        elif self.current == '+':
            return Token(TokenKind.Plus, self.advance())
        elif self.current == '-':
            return Token(TokenKind.Minus, self.advance())
        elif self.current == '*':
            return Token(TokenKind.Star, self.advance())
        elif self.current == '/':
            return Token(TokenKind.Slash, self.advance())
        elif self.current == '(':
            return Token(TokenKind.LParen, self.advance())
        elif self.current == ')':
            return Token(TokenKind.RParen, self.advance())
        elif self.current in '0123456789':
            return self.lex_number()
        elif self.current in 'ij':
            self.advance()
            return Token(TokenKind.Imaginary, Complex(0, 1))
        else:
            return Token(TokenKind.Bad, self.advance())

    def __iter__(self):
        tok = self.next_token()

        while tok.kind != TokenKind.End:
            yield tok
            tok = self.next_token()

        yield tok
