from pathlib import Path
from lexer import tokenize
from parser import Parser

def run_sample(path):
    print(f"Parsing sample: {path}")
    with open(path, 'r') as f:
        code = f.read()
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse_program()
    print(ast)

def main():
    samples = list(Path('sample_programs').glob('*.myl'))
    if not samples:
        print("No sample programs found in sample_programs/")
        return
    run_sample(samples[0])

if __name__ == "__main__":
    main()
