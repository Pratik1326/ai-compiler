import re

# Define token specs (regex for each type)
TOKEN_SPEC = [
    ("NUMBER",   r'\d+(\.\d+)?'),         # int or float
    ("STRING",   r'"[^"]*"'),             # string literal
    ("ID",       r'[A-Za-z_][A-Za-z0-9_]*'),  # identifiers
    ("OP",       r'==|!=|<=|>=|\+|\-|\*|/|%|=|<|>'),  # operators
    ("LPAREN",   r'\('),
    ("RPAREN",   r'\)'),
    ("LBRACE",   r'\{'),
    ("RBRACE",   r'\}'),
    ("SEMICOL",  r';'),
    ("COMMA",    r','),
    ("NEWLINE",  r'\n'),
    ("SKIP",     r'[ \t]+'),              # spaces/tabs
    ("MISMATCH", r'.'),                   # catch bad characters
]

# Keywords
KEYWORDS = {"int", "float", "bool", "string", "if", "else", "while", "return", "func", "print", "input", "true", "false"}

# Token class
class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"

# Lexer function
def tokenize(code):
    tokens = []
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
            tokens.append(Token("NUMBER", value, line_num, column))
        elif kind == "STRING":
            tokens.append(Token("STRING", value[1:-1], line_num, column))
        elif kind == "ID":
            if value in KEYWORDS:
                tokens.append(Token(value.upper(), value, line_num, column))
            else:
                tokens.append(Token("IDENT", value, line_num, column))
        elif kind == "NEWLINE":
            line_num += 1
            line_start = mo.end()
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character {value!r} at line {line_num}, col {column}")
        else:
            tokens.append(Token(kind, value, line_num, column))
    return tokens
