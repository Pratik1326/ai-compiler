# src/main.py
# Minimal runner to confirm project scaffold works.
# We'll replace this with the real CLI after Phase 1.

import sys
from pathlib import Path

def run_sample(path):
    print(f"Running sample: {path}")
    with open(path, 'r') as f:
        print(f.read())

def main():
    samples = list(Path('../sample_programs').glob('*.myl'))
    if not samples:
        print("No sample programs found in sample_programs/")
        return
    # just print the first sample content for now
    run_sample(samples[0])

if __name__ == "__main__":
    main()
