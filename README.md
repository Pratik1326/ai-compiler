# AI-Based Compiler (MiniLang)

Short: a toy language "MiniLang" + AI assistant that explains and suggests fixes for errors.

## How to run (dev)
1. Create & activate venv:
   - python -m venv venv
   - source venv/bin/activate  (Windows: venv\Scripts\activate)
2. Install basics:
   - pip install -r requirements.txt
3. See sample programs in `sample_programs/`

## Project layout
- src/        -> code (lexer, parser, interpreter, ai_assistant)
- sample_programs/ -> example .myl files (correct + buggy)
- notebooks/  -> Colab notebooks for AI experiments
- docs/       -> diagrams and presentation
