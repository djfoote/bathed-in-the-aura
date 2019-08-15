import random

import battle_engine


class PapaRoach(battle_engine.Enemy):
  def __init__(self):
    battle_engine.Enemy.__init__(
        self,
        name='Papa Roach',
        max_hp=20,
        attack=3,
        defense=5,
        sp_attack=1,
        sp_defense=1,
        speed=5)

  def take_turn(self, battle):
    available_actions = ['spawn', 'attack']
    if self.hp >= 2:
      action = random.choice(available_actions)
    else:
      action = 'attack'
    if action == 'attack':
      target = random.choice(battle.players)
      self.attack_target(target)
    elif action == 'spawn':
      lilbug = LilBug('pete')
      print('%s spawned %s' % (self.name, lilbug))
      battle.spawn_enemy(lilbug)
      self.hp //= 2
    self.decrement_auras()

  def get_base_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: 1,
        battle_engine.SPECIAL: 0,
    }[damage_type]


class LilBug(battle_engine.Enemy):
  def __init__(self, identifier):
      battle_engine.Enemy.__init__(
          self,
          name='lil bug %s' % identifier,
          max_hp=5,
          attack=1,
          defense=3,
          sp_attack=1,
          sp_defense=1,
          speed=8)

  def get_base_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: 1,
        battle_engine.SPECIAL: 0,
    }[damage_type]

  def is_interactable(self):
    return True

  def react(self, interactor):
    print("%s bit %s's finger. %s took 1 damage." %
          (self.name, interactor.name, interactor.name))
    interactor.take_damage(1)