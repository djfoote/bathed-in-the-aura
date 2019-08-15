import battle_engine

import enemies
import items
import weapons


def main():
  sword = weapons.Sword('Sword', 2)
  magic_wand = weapons.MagicWand('Magic wand', 2)
  anzacel = battle_engine.Player(
      name='Anzacel',
      max_hp=10,
      attack=10,
      defense=10,
      sp_attack=10,
      sp_defense=10,
      speed=10,
      inventory=[items.BerserkerPotion(), items.Potion(), sword, magic_wand])

  battle = battle_engine.Battle([anzacel], [enemies.PapaRoach()])
  battle.explain()
  battle.start()


if __name__ == '__main__':
  main()