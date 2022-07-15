from utils import *


def grid_values(grid):
  if len(grid) != 81:
    print("Grid must be 81 length")
  else:
    zip_data = zip(boxes,grid)
    my_grid = dict(zip_data)
    for key in my_grid:
      if(my_grid[key] == '.'):
        my_grid[key] = '123456789'
    assert len(my_grid) == 81
    return my_grid