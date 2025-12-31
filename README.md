# Shaded Region Sudoku Solver

An extension of Peter Norvig's classic Sudoku solver to handle puzzles with shaded regions, where each shaded area must also contain digits 1–9 exactly once.

## Contents

- `normal_sudoku.py` – Norvig's original solver adapted to enumerate all solutions.
- `shaded_sudoku.py` – Enhanced solver that parses custom shaded‑region notation and adds shaded areas as extra Sudoku constraints.
- `puzzle_notation.txt` – The original puzzle in custom string format.
- `output_examples/` – Sample outputs from both solvers.

## Puzzle Notation

The puzzle is given in a compact string per row:

- `x` – unknown digit, unshaded
- `a`, `b`, `c`, `d` – cell belongs to shaded region a, b, c, or d
- `=digit` – given digit inside a shaded region (e.g., `a=2`)
- digit without letter – given digit outside any shaded region

Example row: `"x42aaa=8aax"` means:

| Col | 1 | 2 | 3 | 4 | 5 | 6  | 7 | 8 | 9 |
|-----|---|---|---|----|----|----|---|---|---|
| Cell| x | 4 | 2 | a  | a  | a=8| a | a | x |

## How It Works

The shaded‑region solver:

1. **Parses** the custom notation into a shading map and digit map.
2. **Extracts** shaded regions automatically (each region must have exactly 9 cells).
3. **Adds** each shaded region as an extra Sudoku "unit" to Norvig's solver.
4. **Solves** using constraint propagation and search, now enforcing that each shaded region contains 1–9 exactly once.
