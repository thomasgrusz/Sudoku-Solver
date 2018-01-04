import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# ********** Sudoku Solver Part **********
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

# diagonal_units are only used, if the user clicked 'include diagonals' on the website
# If diagnoal_units are used, then unitlist, unit and peers are assigned differently
# in the function solve()
diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))], [rows[i] + cols[(len(rows) - 1) - i] for i in range(len(rows))]]

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


# Convert input from website-form input into a string representation and
# subsequently of puzzle into dictionary
def grid_values(form_puzzle_input):
    puzzle_string = ''
    for field in form_puzzle_input:
        if field:
            puzzle_string += field
        else:
            puzzle_string += '.'
    values = []
    all_digits = '123456789'
    for c in puzzle_string:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


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


# Solve the puzzle with input from web-site, called from SolveHandler()
def solve(values, diag):
    global unitlist
    global units
    global peers
    # Encode the board depending on whether diagonals must be included or not
    if diag == 'yes':
        unitlist = row_units + column_units + square_units + diagonal_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

    # Convert puzzle list from website-form into dictionary
    puzzle_grid_values = grid_values(values)
    solved_puzzle_dict = search(puzzle_grid_values)
    return solved_puzzle_dict


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render("start.html")


class SolveHandler(Handler):
    # Display the values as a 2-D grid. Input: sudoku in dictionary form
    def display(self, values):
        width = 1 + max(len(values[s]) for s in boxes)
        line = ('+'.join(['-' * (width * 3)] * 3)) + '\n'
        for r in rows:
            self.write(''.join(values[r + c].center(width, ' ') + ('|' if c in '36' else '') for c in cols) + '\n')
            if r in 'CF':
                self.write(line)

    def post(self):
        # Comment 'in' to display plain text instead of html on website
        # self.response.headers['Content-Type'] = 'text/plain'

        # Get puzzle info from website as a unicoded list
        puzzle_input = self.request.get_all("field")
        #  Get diagonal-checkbox info from website, 'yes' = include diagnoals, '' = normal Sudoku
        diag = self.request.get("diag")

        # Solve puzzle and return dictionary
        solved_puzzle_dict = solve(puzzle_input, diag)

        # Check if there is a solution to the puzzle
        if solved_puzzle_dict is False:
            self.render("error.html")
        else:
            # Convert puzzle dictionary from search() into list of strings
            solved_puzzle_list = [solved_puzzle_dict[r + c] for r in rows for c in cols]
            # Take puzzle input list from website and convert from unicode to utf-8
            original_puzzle_list = [field.encode('utf-8') if field else '.' for field in puzzle_input]
            # Combine original and solved puzzle lists to a 9x9 list for template rendering
            render_puzzle_list = []
            index_counter = 0
            for tr in range(9):
                render_puzzle_list.append([])
                for td in range(9):
                    if solved_puzzle_list[index_counter] == original_puzzle_list[index_counter]:
                        render_puzzle_list[tr].append([solved_puzzle_list[index_counter], 'original'])
                    else:
                        render_puzzle_list[tr].append([solved_puzzle_list[index_counter], ''])
                    index_counter += 1

            self.render("solution.html", render_puzzle_list=render_puzzle_list)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/solve', SolveHandler)],
    debug=True)
