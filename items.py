import battle_engine


class Potion(battle_engine.Item):
  def get_valid_targets(self, user, battle):
    return battle.players

  def use(self, user, target):
    target.heal(5)
    user.inventory.remove(self)

  def __repr__(self):
    return 'Potion'


class BerserkerPotion(Potion):
  def use(self, user, target):
    berserker_aura = Aura(
    'Berserk',
    {
        (battle_engine.PHYSICAL, battle_engine.ATTACK_DAMAGE_MULTIPLIER): 1.25,
        (battle_engine.PHYSICAL, battle_engine.DEFENDING_DAMAGE_MULTIPLIER): 1.25,
        (battle_engine.SPECIAL, battle_engine.DEFENDING_DAMAGE_MULTIPLIER): 1.25,
    }, duration=3)
    user.auras.append(berserker_aura)
    user.inventory.remove(self)

  def __repr__(self):
    return 'Berserker Potion'