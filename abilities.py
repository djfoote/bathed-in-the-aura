import itertools

import numpy as np

import battle_engine


class Heal(battle_engine.Ability):
  def __init__(self, amount, ap_cost=1, mana_cost=1):
    battle_engine.Ability.__init__(self, 'Heal %d' % amount, ap_cost, mana_cost)
    self.amount = amount

  def use(self, user, battle):
    user.heal(self.amount)


class AreaFlames(battle_engine.Ability):
  def __init__(self, amount, ap_cost=1, mana_cost=1):
    battle_engine.Ability.__init__(
        self, 'Area Flames %d' % amount, ap_cost, mana_cost)
    self.amount = amount

  def use(self, user, battle):
    for enemy in battle.enemies:
      flames_damage = battle_engine.compute_damage(
          power=0,
          strength=0,
          resistance=1,
          damage_bonus=self.amount,
          armor=enemy.get_armor(battle_engine.SPECIAL),
          damage_mult=1,
          received_damage_mult=enemy.get_received_damage_multiplier(
              battle_engine.SPECIAL))
      enemy.take_damage(flames_damage)


class ApplyAura(battle_engine.Ability):
  def __init__(self, name, aura_constructor, ap_cost=1, mana_cost=1):
    battle_engine.Ability.__init__(self, name, ap_cost, mana_cost)
    self.aura_constructor = aura_constructor

  def use(self, user, battle):
    target = battle_engine.choose_option(battle.players + battle.enemies)
    aura = self.aura_constructor()
    target.auras.append(aura)


class AffectStat(ApplyAura):
  def __init__(self, name, target_stat, amount, duration, ap_cost=1,
               mana_cost=1):
    name = '%s %s %s' % (name, *target_stat)
    aura_constructor = lambda: battle_engine.Aura(name,
                                                  {target_stat: amount},
                                                  duration)
    ApplyAura.__init__(self, name, aura_constructor, ap_cost, mana_cost)


class Pray(battle_engine.Ability):
  default_specials = [Heal(1), AreaFlames(1), Heal(2), AreaFlames(2)]

  def __init__(self, buff_add_amount, buff_mult_amount, seal_add_amount,
               seal_mult_amount, duration, specials=None, num_choices=5,
               ap_cost=1, mana_cost=1):
    battle_engine.Ability.__init__(self, 'Pray', ap_cost, mana_cost)

    buffs = self.get_apply_aura_abilities('Buff', buff_add_amount,
                                          buff_mult_amount, duration)
    seals = self.get_apply_aura_abilities('Seal', seal_add_amount,
                                          seal_mult_amount, duration)
    specials = specials if specials is not None else Pray.default_specials
    self.abilities = buffs + seals + specials
    self.num_choices = num_choices

  def get_apply_aura_abilities(self, name, add_amount, mult_amount, duration):
    additive_stats = [battle_engine.POWER, battle_engine.ARMOR]
    multiplicative_stats = [battle_engine.STRENGTH, battle_engine.RESISTANCE]
    additive = [
        AffectStat(name, (damage_type, stat), add_amount, duration)
        for damage_type, stat in itertools.product(battle_engine.DAMAGE_TYPES,
                                                   additive_stats)]
    multiplicative = [
        AffectStat(name, (damage_type, stat), mult_amount, duration)
        for damage_type, stat in itertools.product(battle_engine.DAMAGE_TYPES,
                                                   multiplicative_stats)]
    return additive + multiplicative

  def use(self, user, battle):
    options = np.random.choice(self.abilities, self.num_choices, replace=False)
    ability = battle_engine.choose_option(options)
    ability.use(user, battle)

