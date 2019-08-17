import battle_engine

import abilities
import enemies
import items
import weapons


def main():
  sword = weapons.Sword('Sword', 2)
  magic_wand = weapons.MagicWand('Magic wand', 2)
  anzacel = battle_engine.Player(
      name='Anzacel',
      max_hp=10,
      stat_dict={
          (battle_engine.PHYSICAL, battle_engine.POWER): 1,
          (battle_engine.PHYSICAL, battle_engine.STRENGTH): 2,
          (battle_engine.PHYSICAL, battle_engine.RESISTANCE): 2,
          (battle_engine.PHYSICAL, battle_engine.ARMOR): 0,
          (battle_engine.SPECIAL, battle_engine.POWER): 0.5,
          (battle_engine.SPECIAL, battle_engine.STRENGTH): 2,
          (battle_engine.SPECIAL, battle_engine.RESISTANCE): 1,
          (battle_engine.SPECIAL, battle_engine.ARMOR): 0,
      },
      speed=10,
      inventory=[items.BerserkerPotion(), items.Potion(), sword, magic_wand],
      abilities=[abilities.Pray(0.5, 1.25, 0.5, 0.75, 3)])

  battle = battle_engine.Battle([anzacel],
                                [enemies.PapaRoach(), enemies.HornDog()])
  battle.explain()
  battle.start()


if __name__ == '__main__':
  main()