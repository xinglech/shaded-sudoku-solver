

import time

def cross(A, B):
    return [a+b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)

unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: set(sum(units[s], [])) - {s} for s in squares}

#################### Logging variables ####################
search_nodes = 0
backtracks = 0
solutions_found = 0
####################

def parse_grid(grid):
    values = {s: digits for s in squares}
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign(values, s, d):
    other = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other):
        return values
    return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [sq for sq in u if d in values[sq]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def display(values):
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)

def verify_solution(values):
    """Check all rows, cols, boxes have digits 1-9 exactly once."""
    for r in rows:
        if set(values[r+c] for c in cols) != set(digits):
            return False
    for c in cols:
        if set(values[r+c] for r in rows) != set(digits):
            return False
    for rs in ('ABC','DEF','GHI'):
        for cs in ('123','456','789'):
            if set(values[r+c] for r in rs for c in cs) != set(digits):
                return False
    return True

def solve_all(grid):
    """Return list of all solutions."""
    global search_nodes, backtracks, solutions_found
    search_nodes = backtracks = solutions_found = 0
    
    values = parse_grid(grid)
    if values is False:
        return []
    solutions = []
    search_all(values, solutions)
    print(f"\nSearch stats:")
    print(f"  Search nodes visited: {search_nodes}")
    print(f"  Backtracks (branches explored): {backtracks}")
    print(f"  Solutions found: {solutions_found}")
    return solutions

def search_all(values, solutions):
    global search_nodes, backtracks, solutions_found
    search_nodes += 1
    
    if values is False:
        return
    if all(len(values[s]) == 1 for s in squares):
        if verify_solution(values):
            solutions_found += 1
            solutions.append(values.copy())
        else:
            print("ERROR: Invalid solution generated!")
        return
    
    # Choose square with fewest possibilities > 1
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    branch_count = 0
    for d in values[s]:
        branch_count += 1
        new_values = assign(values.copy(), s, d)
        if new_values is not False:
            search_all(new_values, solutions)
    if branch_count > 1:
        backtracks += (branch_count - 1)  # approximate backtrack count

if __name__ == '__main__':
    # puzzle = (
    #     '.42..8...'
    #     '..8.....5'
    #     '.....2.96'
    #     '4.6.8....'
    #     '...6.1...'
    #     '...9..5.1'
    #     '57.8.....'
    #     '2.....6..'
    #     '...4..95.'
    # )
    puzzle = (
        '.42..8...'
        '..8.....5'
        '.....2896'
        '4.6.8....'
        '...6.1...'
        '...9..561'
        '5748.....'
        '2.....6..'
        '...4..95.'
    )
    print("Finding all normal Sudoku solutions...")
    start = time.time()
    all_solutions = solve_all(puzzle)
    elapsed = time.time() - start
    
    print(f"\nTotal time: {elapsed:.3f} seconds.")
    print(f"Total valid solutions found: {len(all_solutions)}")
    
    # Optional: Show first few solutions
    max_show = 3
    for idx, sol in enumerate(all_solutions[:max_show], 1):
        print(f"\nSolution {idx}:")
        display(sol)
        print("As single-line string:")
        print(''.join(sol[r+c] for r in rows for c in cols))
        print("-" * 30)
    
    if len(all_solutions) > max_show:
        print(f"... and {len(all_solutions) - max_show} more solutions.")

