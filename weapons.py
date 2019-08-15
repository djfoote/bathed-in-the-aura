import battle_engine


class Weapon(battle_engine.Item):
  def __init__(self, name):
    self.name = name

  def get_damage(self, damage_type):
    raise NotImplementedError

  def get_valid_targets(self, user, battle):
    return [user]

  def use(self, user, target):
    print('%s equipped %s' % (user.name, self.name))
    user.equipped = self

  def __repr__(self):
    return self.name


class Sword(Weapon):
  """A basic deterministic physical weapon."""
  def __init__(self, name, base_power):
    Weapon.__init__(self, name)
    self.base_power = base_power

  def get_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: self.base_power,
        battle_engine.SPECIAL: 0,
    }[damage_type]


class MagicWand(Weapon):
  """A basic deterministic special weapon."""
  def __init__(self, name, base_power):
    Weapon.__init__(self, name)
    self.base_power = base_power

  def get_damage(self, damage_type):
    return {
        battle_engine.PHYSICAL: 0,
        battle_engine.SPECIAL: self.base_power,
    }[damage_type]