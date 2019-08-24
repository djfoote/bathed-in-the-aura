import collections

import battle_engine
import choose_grid
import create_character

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
  cells = choose_grid.choose_grid()
  anzacel = create_character.create_character('Anzacel', cells, [])

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