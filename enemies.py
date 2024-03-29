import random

import battle_engine


class PapaRoach(battle_engine.Enemy):
  def __init__(self):
    battle_engine.Enemy.__init__(
        self,
        name='Papa Roach',
        stat_dict={
            (battle_engine.MAX_HP): 20,
            (battle_engine.SPEED): 5,
            (battle_engine.PHYSICAL, battle_engine.POWER): 0,
            (battle_engine.PHYSICAL, battle_engine.STRENGTH): 1,
            (battle_engine.PHYSICAL, battle_engine.RESISTANCE): 1.5,
            (battle_engine.PHYSICAL, battle_engine.ARMOR): 0,
            (battle_engine.SPECIAL, battle_engine.POWER): 0,
            (battle_engine.SPECIAL, battle_engine.STRENGTH): 1,
            (battle_engine.SPECIAL, battle_engine.RESISTANCE): 1,
            (battle_engine.SPECIAL, battle_engine.ARMOR): 0,
        })

  def take_turn(self, battle):
    available_actions = ['spawn', 'attack']
    if self.hp >= 2:
      action = random.choice(available_actions)
    else:
      action = 'attack'
    if action == 'attack':
      target = random.choice(battle.players)
      self.attack_target(target, self.get_standard_attack_tags())
    elif action == 'spawn':
      lilbug = LilBug()
      print('%s spawned %s' % (self.name, lilbug))
      battle.spawn_enemy(lilbug)
      self.hp //= 2
    self.decrement_auras()

  def get_base_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: 2,
        battle_engine.SPECIAL: 0,
    }[damage_type]

  def get_standard_attack_tags(self):
    return [battle_engine.PHYSICAL]


class LilBug(battle_engine.Enemy):
  def __init__(self):
    battle_engine.Enemy.__init__(
        self,
        name='lil bug',
        stat_dict={
            (battle_engine.MAX_HP): 5,
            (battle_engine.SPEED): 8,
            (battle_engine.PHYSICAL, battle_engine.POWER): 0,
            (battle_engine.PHYSICAL, battle_engine.STRENGTH): 1,
            (battle_engine.PHYSICAL, battle_engine.RESISTANCE): 1.5,
            (battle_engine.PHYSICAL, battle_engine.ARMOR): 0,
            (battle_engine.SPECIAL, battle_engine.POWER): 0,
            (battle_engine.SPECIAL, battle_engine.STRENGTH): 1,
            (battle_engine.SPECIAL, battle_engine.RESISTANCE): 1,
            (battle_engine.SPECIAL, battle_engine.ARMOR): 0,
        })

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

  def get_standard_attack_tags(self):
    return [battle_engine.PHYSICAL]


class HornDog(battle_engine.Enemy):
  def __init__(self):
    battle_engine.Enemy.__init__(
        self,
        name='Horn Dog',
        stat_dict={
            (battle_engine.MAX_HP): 10,
            (battle_engine.SPEED): 11,
            (battle_engine.PHYSICAL, battle_engine.POWER): 0,
            (battle_engine.PHYSICAL, battle_engine.STRENGTH): 1,
            (battle_engine.PHYSICAL, battle_engine.RESISTANCE): 1,
            (battle_engine.PHYSICAL, battle_engine.ARMOR): 0,
            (battle_engine.SPECIAL, battle_engine.POWER): 0,
            (battle_engine.SPECIAL, battle_engine.STRENGTH): 1,
            (battle_engine.SPECIAL, battle_engine.RESISTANCE): 1,
            (battle_engine.SPECIAL, battle_engine.ARMOR): 0,
        })

    self.thorns_damage = 1

  def get_base_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: 1.5,
        battle_engine.SPECIAL: 0,
    }[damage_type]

  def get_standard_attack_tags(self):
    return [battle_engine.PHYSICAL]

  def respond_to_attack(self, attacker):
    thorns_damage = round(battle_engine.compute_damage(
        power=0,
        strength=0,
        resistance=1,
        damage_bonus=self.thorns_damage,
        armor=attacker.get_armor(battle_engine.PHYSICAL),
        damage_mult=1,
        received_damage_mult=attacker.get_received_damage_multiplier(
            battle_engine.PHYSICAL)))
    print('%s dealt %d thorns damage' % (self.name, thorns_damage))
    attacker.take_damage(thorns_damage)
