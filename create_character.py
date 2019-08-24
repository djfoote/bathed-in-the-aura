import battle_engine
import grid_cells

import abilities
import items
import weapons


DEFAULT_STATS = {
    (battle_engine.MAX_HP): 10,
    (battle_engine.MAX_MANA): 10,
    (battle_engine.SPEED): 10,
    (battle_engine.PHYSICAL, battle_engine.POWER): 0,
    (battle_engine.PHYSICAL, battle_engine.STRENGTH): 1,
    (battle_engine.PHYSICAL, battle_engine.RESISTANCE): 1,
    (battle_engine.PHYSICAL, battle_engine.ARMOR): 0,
    (battle_engine.SPECIAL, battle_engine.POWER): 0,
    (battle_engine.SPECIAL, battle_engine.STRENGTH): 1,
    (battle_engine.SPECIAL, battle_engine.RESISTANCE): 1,
    (battle_engine.SPECIAL, battle_engine.ARMOR): 0,
}
DEFAULT_PRAY_OPTIONS = 3


def create_character(name, cells, inventory):
  stats = update_stats(DEFAULT_STATS.copy(), cells)
  pray_ability = create_pray_ability(cells)
  return battle_engine.Player(
      name=name,
      stat_dict=stats,
      inventory=inventory,
      abilities=[pray_ability])


def update_stats(stats, cells):
  for cell in cells:
    if isinstance(cell, grid_cells.AddStats):
      for stat, amount in cell.stats_dict.items():
        stats[stat] += amount
    elif isinstance(cell, grid_cells.MultiplyStats):
      for stat, amount in cell.stats_dict.items():
        stats[stat] *= amount
  return stats


def create_pray_ability(cells):
  num_pray_options = DEFAULT_PRAY_OPTIONS
  for cell in cells:
    if isinstance(cell, grid_cells.IncreaseNumberOfPrayOptions):
      num_pray_options += cell.amount

  special_spells = []
  for cell in cells:
    if isinstance(cell, grid_cells.AddPraySpells):
      special_spells.extend(cell.spells)

  return abilities.Pray(specials=special_spells, num_choices=num_pray_options)
