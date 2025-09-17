# src/ai_assistant.py
import re
import difflib
from typing import Tuple, Optional

# ---------- Helpers ----------

def _extract_line_num_from_msg(msg: str) -> Optional[int]:
    m = re.search(r'line (\d+)', msg)
    if m:
        return int(m.group(1))
    return None

def _get_lines(code: str):
    return code.splitlines()

def _all_identifiers(code: str):
    # crude identifier extraction
    return re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', code)

# ---------- Explanations & Fixes (rule-based) ----------

def explain_error(exc: Exception) -> str:
    """Return a short human-friendly explanation for an exception."""
    msg = str(exc)
    if 'Expected SEMICOL' in msg or 'Expected SEMICOL' in msg.upper():
        return "It looks like a statement is missing a semicolon (`;`) at the end."
    if 'Expected RPAREN' in msg or 'Expected RPAREN' in msg.upper():
        return "A closing parenthesis `)` is missing."
    if 'Expected RBRACE' in msg or 'Expected RBRACE' in msg.upper():
        return "A closing brace `}` is missing (maybe you forgot to close a block)."
    if 'Unexpected token' in msg:
        return "There's an unexpected token at the mentioned location — maybe a typo or missing punctuation."
    if isinstance(exc, NameError) and "Variable" in msg or "variable" in msg.lower():
        return "A variable or function name is used but not defined. Maybe you misspelled it or forgot a declaration."
    if isinstance(exc, TypeError):
        return "A type error occurred — argument counts or operand types may be incorrect."
    # fallback
    return "Error: " + msg

def suggest_fix(code: str, exc: Exception) -> Tuple[Optional[str], str]:
    """
    Try to create a simple fix for the code given the exception.
    Returns: (fixed_code or None if no automatic fix, description_of_fix)
    """
    msg = str(exc)
    lines = _get_lines(code)

    # --- Missing semicolon (Expected SEMICOL) ---
    if 'Expected SEMICOL' in msg:
        line_no = _extract_line_num_from_msg(msg) or 1
        # if parser says semicolon expected at line L, try adding ; at end of that line
        idx = max(0, line_no - 1)
        fixed_lines = lines.copy()
        # only add if line does not already end with ; or { or }
        if not fixed_lines[idx].rstrip().endswith((';', '{', '}')):
            fixed_lines[idx] = fixed_lines[idx] + ';'
            return ("\n".join(fixed_lines), f"Inserted ';' at end of line {line_no}.")

    # --- Missing parenthesis (Expected RPAREN) ---
    if 'Expected RPAREN' in msg or 'got RPAREN' in msg:
        line_no = _extract_line_num_from_msg(msg) or 1
        idx = max(0, line_no - 1)
        fixed_lines = lines.copy()
        fixed_lines[idx] = fixed_lines[idx] + ')'
        return ("\n".join(fixed_lines), f"Inserted ')' at end of line {line_no}.")

    # --- Missing brace (Expected RBRACE) ---
    if 'Expected RBRACE' in msg:
        # append a closing brace at end of file
        fixed = code + "\n}"
        return (fixed, "Appended a '}' at the end of the file (closing a block).")

    # --- Undefined variable / function (NameError) ---
    if isinstance(exc, NameError):
        # parse the name from the message (try common formats)
        m = re.search(r"[Vv]ariable '([^']+)'|Function '([^']+)'|variable '([^']+)'", msg)
        name = None
        if m:
            name = next(g for g in m.groups() if g)
        else:
            # fallback: pick last word
            parts = msg.split()
            if parts:
                name = parts[-1].strip("'.")
        if name:
            idents = list(set(_all_identifiers(code)))
            candidates = difflib.get_close_matches(name, idents, n=3, cutoff=0.6)
            if candidates:
                return (None, f"Name '{name}' not defined. Did you mean: {', '.join(candidates)}?")
            else:
                return (None, f"Name '{name}' not defined. Check for missing declaration or typo.")
        return (None, "Name not defined. Check for missing declaration or typo.")

    # --- Type / arg count issues (TypeError) ---
    if isinstance(exc, TypeError):
        # short friendly message; auto-fix is risky
        return (None, "Type error or wrong number of function arguments. Please verify types/arg counts.")

    # --- Fallback: no automatic fix ---
    return (None, "No automatic fix found. Try correcting the code near the mentioned line.")

# Convenience function for full pipeline
def explain_and_suggest(code: str, exc: Exception) -> Tuple[str, Optional[str]]:
    """
    Returns (explanation, suggestion_text) where suggestion_text is either a description or
    a string asking to apply a fix. If a fix is available, it's returned as the second element *and*
    stored as text (not automatically applied here).
    """
    explanation = explain_error(exc)
    fixed_code, fix_note = suggest_fix(code, exc)
    if fixed_code:
        return (explanation, f"Suggested fix: {fix_note}\n\n--- Fixed Code Preview ---\n{fixed_code}")
    else:
        return (explanation, fix_note)
