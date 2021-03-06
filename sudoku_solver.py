# SUDOKU Solver
# Project 1 in the Udacity Artificial Intelligence Nanodegree


# ---- Board Setup ----
# A sudoku puzzle consists of a 9x9 grid of boxes, filled with digits from 1 - 9.

# We label 3 distinct entities in the board.

# boxes - the individual boxes in the board(9x9=81)
# units - rows, columns and the subsquares(3 x 9=27)
# peers - a box has peers in a row a column and a subsquare(8 + 6 + 6=20)


# ---- Encoding the board ----
# Rows will be labeled from 'A-I'
# Columns will be labeled from '1-9'

# A board will be encoded in two ways.
# 1. a long string with box contents in a series from left to right, top to bottom
# 2. a dictionary with box labels as keys, i.e. 'A1' and the box contents as values

# For both encodings, the values for empty boxes is a '.' (period).

rows = 'ABCDEFGHI'
cols = '123456789'


# cross() helper function creates all combinations of letters in 2 strings
def cross(a, b):
    return [r + c for r in a for c in b]


# Create lists of boxes, row_units, column_units, square_units
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units

units = dict()
for s in boxes:
    x = []
    for u in unitlist:
        if s in u:
            x.append(u)
    units[s] = x

peers = dict()
for s in boxes:
    x = set(sum(units[s], [])) - set([s])
    peers[s] = x

# units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# peers = {s: set(sum(units[s], [])) - set([s]) for s in boxes}
# This is udacity's dict comprehension to create the 'peers' dict
# peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


# Convert string representation of puzzle into dictionary
def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


# Display the values as a 2-D grid. Input: sudoku in dictionary form
def display(values):
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width, ' ') + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)


# --- Elimination strategy ---
# The eliminate() function will eliminate search boxes with a single digit and
# eliminate that digit from its peers.
def eliminate(values):
    for box in values.keys():
        if len(values[box]) == 1:
            elimination_value = values[box]
            for peer in peers[box]:
                values[peer] = values[peer].replace(elimination_value, '')
    return values


# --- Only choice strategy ---
# The function will go through all the units, and if there is a unit with a
# digit that only fits in one possible box, it will assign that digit to that
# box.
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


# ---- Reduce puzzle by constraint propagation ----
# Repeatedly apply the eliminate() and only_choice() functions until the puzzle
# is solved. This is called 'Constraint Propagation'
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        eliminate(values)
        only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        # Sanity check for boxes with zero available values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# "Using depth-first search and propagation, try all possible values."


def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


# Test code above
puzzle_1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
puzzle_2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

print('SUDOKU 1')
puzzle_1 = grid_values(puzzle_1)
display(search(puzzle_1))

print()

print('SUDOKU 2')
puzzle_2 = grid_values(puzzle_2)
display(search(puzzle_2))

print()
