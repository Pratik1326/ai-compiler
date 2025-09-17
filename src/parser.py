from lexer import tokenize, Token

# ---------------- AST NODE CLASSES ----------------

class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class VarDecl(Node):
    def __init__(self, var_type, name, value=None):
        self.var_type = var_type
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VarDecl({self.var_type}, {self.name}, {self.value})"

class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class Print(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Print({self.expr})"

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Literal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"

class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class FuncDecl(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FuncDecl({self.name}, params={self.params}, body={self.body})"

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Return({self.expr})"

# ---------------- PARSER ----------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type=None):
        tok = self.current()
        if tok is None:
            return None
        if token_type and tok.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {tok.type} at line {tok.line}")
        self.pos += 1
        return tok

    # program ::= { statement }
    def parse_program(self):
        statements = []
        while self.current() is not None:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    # statement ::= var_decl | assignment | print_stmt | func_decl | return_stmt
    def parse_statement(self):
        tok = self.current()
        if tok.type in {"INT", "FLOAT", "BOOL", "STRING"}:
            return self.parse_var_decl()
        elif tok.type == "IDENT":
            return self.parse_assignment()
        elif tok.type == "PRINT":
            return self.parse_print()
        elif tok.type == "FUNC":
            return self.parse_func_decl()
        elif tok.type == "RETURN":
            return self.parse_return()
        else:
            raise SyntaxError(f"Unexpected token {tok.type} at line {tok.line}")

    # var_decl ::= type IDENT [= expr] ;
    def parse_var_decl(self):
        var_type = self.eat().value
        name_tok = self.eat("IDENT")
        value = None
        if self.current() and self.current().type == "OP" and self.current().value == "=":
            self.eat("OP")
            value = self.parse_expr()
        self.eat("SEMICOL")
        return VarDecl(var_type, name_tok.value, value)

    # assignment ::= IDENT = expr ;
    def parse_assignment(self):
        name_tok = self.eat("IDENT")
        self.eat("OP")  # assume '='
        value = self.parse_expr()
        self.eat("SEMICOL")
        return Assignment(name_tok.value, value)

    # print_stmt ::= print ( expr ) ;
    def parse_print(self):
        self.eat("PRINT")
        self.eat("LPAREN")
        expr = self.parse_expr()
        self.eat("RPAREN")
        self.eat("SEMICOL")
        return Print(expr)

    # return_stmt ::= return expr ;
    def parse_return(self):
        self.eat("RETURN")
        expr = self.parse_expr()
        self.eat("SEMICOL")
        return Return(expr)

    # func_decl ::= "func" IDENT "(" [param_list] ")" "{" { stmt } "}"
    def parse_func_decl(self):
        self.eat("FUNC")
        name_tok = self.eat("IDENT")
        self.eat("LPAREN")
        params = []
        if self.current().type != "RPAREN":
            params.append(self.eat("IDENT").value)
            while self.current() and self.current().type == "COMMA":
                self.eat("COMMA")
                params.append(self.eat("IDENT").value)
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = []
        while self.current() and self.current().type != "RBRACE":
            stmt = self.parse_statement()
            body.append(stmt)
        self.eat("RBRACE")
        return FuncDecl(name_tok.value, params, body)

    # expr ::= NUMBER | IDENT | (expr) | expr OP expr
    def parse_expr(self):
           # Start with a term (number, identifier, or parenthesized expression)
        left = self.parse_term()
    # Handle binary operators (left-to-right)
        while self.current() and self.current().type == "OP":
              op_tok = self.eat("OP")
              right = self.parse_term()
              left = BinOp(left, op_tok.value, right)
              return left

    def parse_term(self):
        tok = self.current()
        if tok.type == "NUMBER":
            self.eat("NUMBER")
            return Literal(tok.value)
        elif tok.type == "STRING":
            self.eat("STRING")
            return Literal(tok.value)
        elif tok.type == "IDENT":
            self.eat("IDENT")
            return Identifier(tok.value)
        elif tok.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.parse_expr()
            self.eat("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token {tok.type} at line {tok.line}")

      