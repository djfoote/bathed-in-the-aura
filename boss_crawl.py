import collections

import battle_engine

import abilities
import enemies
import items
import weapons


DIFFICULTY = 'easy'

BOSSES = {
  'papa roach': enemies.PapaRoach,
  'horn dog': enemies.HornDog,
}


def create_battle(anzacel, encounter):
  battle_enemies = []
  if not encounter:
    return battle_engine.Battle([anzacel], [enemies.LilBug()])
  for boss, number in encounter.items():
    for _ in range(number):
      battle_enemies.append(BOSSES[boss]())
  return battle_engine.Battle([anzacel], battle_enemies)


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

  encounter = collections.Counter()
  score = 0
  battle = create_battle(anzacel, encounter)
  while battle.start():
    score += 1
    print('Your current score: %d' % score)
    print()

    if DIFFICULTY == 'hard':
      if score % 3 == 2:
        encounter['papa roach'] -= 1
        encounter['horn dog'] += 1
      else:
        encounter['papa roach'] += 1  
      battle = create_battle(anzacel, encounter)

    elif DIFFICULTY == 'easy':
      enemy = enemies.PapaRoach() if score % 2 == 1 else enemies.HornDog()
      battle = battle_engine.Battle([anzacel], [enemy])

    else:
      raise ValueError('Invalid difficulty %s' % DIFFICULTY)


  print('Game over. Your score: %d' % score)

if __name__ == '__main__':
  main()