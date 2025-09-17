# MiniLang – Language Specification

## 1. Overview
MiniLang is a toy programming language designed for educational purposes and compiler construction practice. It features simple syntax, static typing, basic control structures, and user-defined functions.
Our project extends MiniLang with AI-assisted compilation: when errors occur, the compiler will explain them in plain English and optionally suggest or apply fixes.

## 2. Design Goals
- Simple but expressive syntax (C/Python-like).
- Easy to parse and implement in a short project timeline.
- Rich enough to demonstrate variables, expressions, control flow, and functions.
- Strict grammar to trigger common beginner mistakes (useful for AI explanations).

## 3. Data Types
- `int`, `float`, `bool`, `string`

## 4. Keywords
int, float, bool, string, if, else, while, return, func, print, input, true, false

## 5. Operators
+ - * / % ,  == != < > <= >= , && || !

## 6. Comments
// single-line
/* multi-line */

## 7. Grammar (EBNF-style)
program     ::= { top_decl | stmt }
top_decl    ::= func_decl
func_decl   ::= "func" IDENT "(" [param_list] ")" "{" { stmt } "}"
param_list  ::= IDENT { "," IDENT }

stmt        ::= var_decl ";" 
              | assignment ";" 
              | "print" "(" expr ")" ";"
              | "if" "(" expr ")" "{" { stmt } "}" [ "else" "{" { stmt } "}" ]
              | "while" "(" expr ")" "{" { stmt } "}"
              | "return" expr ";"

var_decl    ::= type IDENT [ "=" expr ]
type        ::= "int" | "float" | "bool" | "string"

assignment  ::= IDENT "=" expr

expr        ::= logic_or
logic_or    ::= logic_and { "||" logic_and }
logic_and   ::= equality { "&&" equality }
equality    ::= relational { ("==" | "!=") relational }
relational  ::= additive { ("<" | ">" | "<=" | ">=") additive }
additive    ::= multiplicative { ("+" | "-") multiplicative }
multiplicative ::= unary { ("*" | "/" | "%") unary }
unary       ::= ("+" | "-" | "!") unary | primary
primary     ::= NUMBER | STRING | IDENT | "(" expr ")" | func_call
func_call   ::= IDENT "(" [ arg_list ] ")"
arg_list    ::= expr { "," expr }

## 8. Example Programs
### Hello / arithmetic
int a = 5;
int b = a * 2 + 3;
print(b);

### If/while
int n = 5;
int i = 0;
int sum = 0;
while (i < n) {
  sum = sum + i;
  i = i + 1;
}
if (sum > 10) {
  print(sum);
} else {
  print(0);
}

### Function
func add(x, y) {
  return x + y;
}
int r = add(3, 4);
print(r);

### Buggy (for AI demo)
int a = 5
print(a

Expected AI suggestion:
- Add missing `;` after `5`
- Add `)` after `print(a)`

## 9. Error Types (for AI Assistant)
- Syntax errors: missing semicolons, mismatched parentheses/braces, unexpected tokens.
- Name errors: undefined variables or functions.
- Type errors: incompatible operations (e.g., adding string to int).
- Runtime errors: division by zero (optional).

## 10. Execution Model
- Programs execute top-to-bottom.
- Functions must be declared before they are called.
- Variables are statically typed.
- The compiler will either run the program (if correct) or display errors (with AI-based explanations if enabled).
