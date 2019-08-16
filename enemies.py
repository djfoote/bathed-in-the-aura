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


class HornDog(battle_engine.Enemy):
  def __init__(self):
    battle_engine.Enemy.__init__(
        self,
        name='Horn Dog',
        max_hp=10,
        attack=5,
        defense=3,
        sp_attack=1,
        sp_defense=2,
        speed=11)

    self.thorns_damage = 1

  def get_base_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: 1,
        battle_engine.SPECIAL: 0,
    }[damage_type]

  def respond_to_attack(self, attacker):
    thorns_damage = battle_engine.compute_damage(
        base_damage=0,
        attack_mult=0,
        def_mult=0,
        damage_bonus=self.thorns_damage,
        def_bonus=attacker.get_def_bonus(battle_engine.PHYSICAL),
        atk_damage_mult=1,
        def_damage_mult=attacker.get_defending_damage_multiplier(
            battle_engine.PHYSICAL))
    print('%s dealt %d thorns damage' % (self.name, thorns_damage))
    attacker.take_damage(thorns_damage)
