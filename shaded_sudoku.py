import time

def cross(A, B):
    return [a+b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)

# Standard Sudoku units
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

#################### PARSE AND EXTRACT SHADED REGIONS ####################
def parse_puzzle():
    raw_rows = [
        "x42aaa=8aax",
        "bx8xaaax5",
        "bbxxxa=2x96",
        "b=4bb=6x8xxxd",
        "bbx6x1xdd",
        "bxxx9xd=5dd=1",
        "57xc=8xxxdd",
        "2xcccx6xd",
        "xccc=4cc95x"
    ]
    
    shading_map = {}
    digit_map = {}
    
    for r_idx, raw in enumerate(raw_rows):
        r = rows[r_idx]
        c_idx = 0
        i = 0
        while i < len(raw) and c_idx < 9:
            ch = raw[i]
            if ch in 'abcd':
                region = ch
                if i+1 < len(raw) and raw[i+1] == '=':
                    digit = raw[i+2]
                    shading_map[r + cols[c_idx]] = region
                    digit_map[r + cols[c_idx]] = digit
                    i += 3
                else:
                    shading_map[r + cols[c_idx]] = region
                    digit_map[r + cols[c_idx]] = '.'
                    i += 1
                c_idx += 1
            elif ch == '=':
                i += 1
            elif ch in digits:
                shading_map[r + cols[c_idx]] = '.'
                digit_map[r + cols[c_idx]] = ch
                i += 1
                c_idx += 1
            elif ch == 'x':
                shading_map[r + cols[c_idx]] = '.'
                digit_map[r + cols[c_idx]] = '.'
                i += 1
                c_idx += 1
            else:
                i += 1
    return shading_map, digit_map

shading_map, digit_map = parse_puzzle()

# Extract shaded regions from shading_map
from collections import defaultdict
region_to_cells = defaultdict(list)
for cell, region in shading_map.items():
    if region != '.':
        region_to_cells[region].append(cell)

shaded_regions = list(region_to_cells.values())
print("Extracted shaded regions (counts):")
for region in shaded_regions:
    print(f"{len(region)} cells:", sorted(region))

# Add to unitlist
unitlist += shaded_regions
#################### END EXTRACTION ####################

units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: set(sum(units[s], [])) - {s} for s in squares}

#################### DISPLAY ####################
def display_puzzle():
    print("\nPuzzle grid (shaded regions a,b,c,d shown as letters, digits shown):")
    print("  1 2 3   4 5 6   7 8 9")
    for r in rows:
        line = f"{r} "
        for c in cols:
            cell = r + c
            d = digit_map.get(cell, '.')
            s = shading_map.get(cell, '.')
            if s != '.':
                if d != '.':
                    line += f"\033[47m{d}\033[0m "
                else:
                    line += f"\033[47m{s}\033[0m "
            else:
                if d != '.':
                    line += f"{d} "
                else:
                    line += ". "
            if c in '36':
                line += "| "
        print(line)
        if r in 'CF':
            print("  ------+-------+------")

#################### SOLVER ####################
search_nodes = 0
backtracks = 0
solutions_found = 0

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
    for u in unitlist:
        if set(values[s] for s in u) != set(digits):
            return False
    return True

def solve_all(grid):
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
    
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    branch_count = 0
    for d in values[s]:
        branch_count += 1
        new_values = assign(values.copy(), s, d)
        if new_values is not False:
            search_all(new_values, solutions)
    if branch_count > 1:
        backtracks += (branch_count - 1)

if __name__ == '__main__':
    display_puzzle()
    
    # Build grid string from digit_map
    grid_chars = []
    for r in rows:
        for c in cols:
            grid_chars.append(digit_map.get(r + c, '.'))
    puzzle = ''.join(grid_chars)
    
    print("\nGrid string:", puzzle)
    print("\n" + "="*50)
    print("Solving with extracted shaded regions...")
    
    start = time.time()
    all_solutions = solve_all(puzzle)
    elapsed = time.time() - start
    
    print(f"\nTotal time: {elapsed:.3f} seconds.")
    print(f"Total valid solutions (with shaded regions): {len(all_solutions)}")
    
    if all_solutions:
        print("\n--- Solution(s) ---")
        for idx, sol in enumerate(all_solutions, 1):
            print(f"\nSolution {idx}:")
            display(sol)
            print("As single-line string:")
            print(''.join(sol[r+c] for r in rows for c in cols))
            print("-" * 30)
    else:
        print("\nNo solution found.")