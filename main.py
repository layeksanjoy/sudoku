import time
start_time = time.time()

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
# grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'

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

def elimination(values):
  # sudo = grid_values(grid)
  # # print(sudo)
  # for i in boxes:
  #   if(len(sudo[i]) == 1):
  #     continue
  #   else:
  #     for j in peers[i]:
  #       value = ""
  #       if(len(sudo[j]) == 1):
  #           #remove that element from sudo[i]
  #           for k in sudo[i]:
  #             if(k == sudo[j]):
  #               continue
  #             else:
  #               value = value + k
  #           sudo[i] = value

  for box in values.keys():
    if len(values[box]) == 1:
      for peer_box in peers[box]:
        values[peer_box] = values[peer_box].replace(values[box],'')
  
  return values

def only_choice(value):
  """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
  for unit in units:
    u = units[unit][2]
    for i in u:
      if len(value[i]) != 1:
        #check if unique
        unique = 1
        for k in value[i]:
          for j in u:
            if(i != j) and k in value[j]:
              unique = 0
              break
          if(unique  == 1):
            value[i] = k
  return value

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = elimination(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    
    node = ''
    min = 10
    for k in values.keys():
      if len(values[k]) < min and len(values[k]) > 1:
        min = len(values[k])
        node = k
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    if(node != ''):
      for i in values[node]:
        new_sodu = values.copy()
        new_sodu[node] = i
        attempt = search(new_sodu)
        if attempt : 
          return attempt

    # If you're stuck, see the solution.py tab!
values = grid_values(grid)
t=search(values)
display(t)


print("\n\n TIme Taken %s seconds " % (time.time() - start_time))
