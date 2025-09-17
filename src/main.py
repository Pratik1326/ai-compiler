from pathlib import Path
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter
from ai_assistant import explain_and_suggest

def run_file_with_assistant(path, auto_apply=False):
    print(f"\n=== Running file: {path} ===")
    with open(path, 'r') as f:
        code = f.read()

    # Try parse + run, and catch errors
    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse_program()
        print("AST:", ast)
        print("\n--- Running Interpreter ---")
        interp = Interpreter()
        interp.eval_program(ast)
        print("\nProgram finished successfully.")
        return True
    except Exception as e:
        print("\n--- Error caught ---")
        print(type(e).__name__ + ":", e)
        explanation, suggestion = explain_and_suggest(code, e)
        print("\nAssistant explanation:")
        print("-", explanation)
        print("\nAssistant suggestion:")
        print("-", suggestion)
        if suggestion and suggestion.startswith("Suggested fix"):
            # If assistant returned a fixed code preview, extract fixed code text portion
            m = suggestion.split("\n\n--- Fixed Code Preview ---\n", 1)
            if len(m) == 2:
                fixed_code = m[1]
                if auto_apply:
                    # overwrite file with fixed code and re-run
                    print("\nAuto-applying fix and re-running...")
                    with open(path, "w") as f:
                        f.write(fixed_code)
                    return run_file_with_assistant(path, auto_apply=False)
                else:
                    print("\nTo apply this fix automatically, call run with auto_apply=True")
        return False

def main():
    samples = list(Path('sample_programs').glob('*.myl'))
    if not samples:
        print("No sample programs found in sample_programs/")
        return

    # run each file once (no auto-apply by default)
    for p in samples:
        run_file_with_assistant(p, auto_apply=False)

if __name__ == "__main__":
    main()
