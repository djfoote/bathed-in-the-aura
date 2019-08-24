try:
  import networkx as nx
  import matplotlib.pyplot as plt
except ImportError:
  nx = None
  plt = None

import battle_engine
import grid_cells

import abilities


class Node():
  def __init__(self, grid_cell):
    self.grid_cell = grid_cell
    self.children = []

  def __repr__(self):
    return repr(self.grid_cell)


def convert_nx_graph(root):
  graph = nx.Graph()
  graph.add_node(root.grid_cell)
  parent = root
  queue = [root]
  while queue:
    node = queue.pop()
    for child in node.children:
      graph.add_node(child.grid_cell)
      graph.add_edge(node.grid_cell, child.grid_cell)
      queue.append(child)
  return graph


def show_nx_graph(graph):
  nx.draw(graph, with_labels=True, font_weight='bold')
  plt.show()


def construct_grid():
  root = Node(grid_cells.GridCell('Root'))
  max_hp_2 = Node(grid_cells.AddStats('Max HP +2', {battle_engine.MAX_HP: 2}))
  max_mana_2 = Node(grid_cells.AddStats('Max Mana +2',
                                        {battle_engine.MAX_MANA: 2}))
  speed_2 = Node(grid_cells.AddStats('Speed +2', {battle_engine.SPEED: 2}))
  phys_power_1 = Node(grid_cells.AddStats(
      'Physical Power +1', {(battle_engine.PHYSICAL,
                             battle_engine.POWER): 1}))
  phys_strength_2 = Node(grid_cells.MultiplyStats(
      'Physical Strength *2', {(battle_engine.PHYSICAL,
                                battle_engine.STRENGTH): 2}))
  phys_res_2 = Node(grid_cells.MultiplyStats(
      'Physical Resistance *2', {(battle_engine.PHYSICAL,
                                  battle_engine.RESISTANCE): 2}))
  heal_1_2 = Node(grid_cells.AddPraySpells(
      'Heal 1-2',
      [abilities.Heal(1), abilities.Heal(2)]))
  area_flames_1_2 = Node(grid_cells.AddPraySpells(
      'Area Flames 1-2',
      [abilities.AreaFlames(1), abilities.AreaFlames(2)]))
  increase_pray_options_1_1 = Node(grid_cells.IncreaseNumberOfPrayOptions(
      'Pray Options +1', 1))
  increase_pray_options_1_2 = Node(grid_cells.IncreaseNumberOfPrayOptions(
      'Pray Options +1', 1))

  root.children = [max_hp_2, max_mana_2]
  max_hp_2.children = [phys_power_1, phys_strength_2]
  phys_strength_2.children = [phys_res_2]
  phys_power_1.children = [speed_2]
  max_mana_2.children = [heal_1_2, area_flames_1_2]
  heal_1_2.children = [increase_pray_options_1_1]
  area_flames_1_2.children = [increase_pray_options_1_2]


  return root


grid = construct_grid()


if __name__ == '__main__':
  if nx is not None and plt is not None:
    graph = convert_nx_graph(grid)
    show_nx_graph(graph)
