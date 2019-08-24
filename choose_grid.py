import battle_engine
import grid

DEFAULT_NUM_POINTS = 5


def choose_grid(num_points=DEFAULT_NUM_POINTS):
  cells = []
  options = grid.grid.children
  while num_points and options:
    cell = battle_engine.choose_option(options)
    cells.append(cell.grid_cell)
    options.remove(cell)
    options.extend(cell.children)
    num_points -= 1
  return cells