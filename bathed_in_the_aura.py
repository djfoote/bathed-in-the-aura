import collections
import random

MAX_ACTION_POINTS = 3

CRIT_PROBABILITY = 1/8
CRIT_MULTIPLIER = 2

# Placeholder stat system: multipliers are `STAT_EXPONENT_BASE ** stat_value`.
STAT_EXPONENT_BASE = 1.1

# Damage types
PHYSICAL = 'physical'
SPECIAL = 'special'

# Effect keys
BASE_DAMAGE_BONUS = 'base_damage_bonus'
ATTACK_MULTIPLIER = 'attack_multiplier'
DEFENSE_MULTIPLIER = 'defense_multiplier'
FLAT_DAMAGE_BONUS = 'flat_damage_bonus'
FLAT_DEFENSE_BONUS = 'flat_defense_bonus'
ATTACK_DAMAGE_MULTIPLIER = 'attack_damage_multiplier'
DEFENDING_DAMAGE_MULTIPLIER = 'defending_damage_multiplier'

# Aggregation methods
ADD = 'add'
MULT = 'mult'


class Actor():
  def __init__(self, name, max_hp, attack, defense, sp_attack, sp_defense,
               speed, auras=None):
    self.name = name

    self.max_hp = max_hp
    self.hp = max_hp
    self.alive = True

    self.attack = attack
    self.defense = defense
    self.sp_attack = sp_attack
    self.sp_defense = sp_defense
    self.speed = speed

    if auras is None:
      self.auras = []
    else:
      self.auras = auras

  def take_damage(self, damage):
    self.hp -= damage
    self.hp = max(self.hp, 0)
    print('%s has %d hp remaining.' % (self.name, self.hp))
    if self.hp <= 0:
      self.die()

  def heal(self, amount):
    self.hp += amount
    self.hp = min(self.hp, self.max_hp)
    print('%s has %d hp remaining.' % (self.name, self.hp))

  def die(self):
    self.alive = False
    print('%s died' % self.name)

  def __repr__(self):
    return self.name

  def attack_target(self, target):
    phys_damage = self.get_damage(target, PHYSICAL)
    sp_damage = self.get_damage(target, SPECIAL)
    crit = random.random() < CRIT_PROBABILITY
    crit_multiplier = CRIT_MULTIPLIER if crit else 1

    damage = round((phys_damage + sp_damage) * crit_multiplier)

    print('%s attacked %s.' % (self.name, target.name))
    if crit:
      print('Critical hit!')
    print('%s took %d damage.' % (target.name, damage))

    target.take_damage(damage)

  def get_damage(self, target, damage_type):
    base_damage = self.get_base_damage(damage_type)
    base_damage += self.get_base_damage_bonus(damage_type)
    attack_mult = self.get_attack_multiplier(damage_type)
    def_mult = target.get_defense_multiplier(damage_type)
    damage_bonus = self.get_damage_bonus(damage_type)
    def_bonus = target.get_def_bonus(damage_type)
    atk_damage_mult = self.get_attack_damage_multiplier(damage_type)
    def_damage_mult = target.get_defending_damage_multiplier(damage_type)

    raw_phys_damage = (
        base_damage * attack_mult * def_mult + damage_bonus - def_bonus)

    return max(0, raw_phys_damage) * atk_damage_mult * def_damage_mult

  def get_base_damage(self, damage_type):
    raise NotImplementedError

  def get_base_damage_bonus(self, damage_type):
    return self.get_aura_effect((damage_type, BASE_DAMAGE_BONUS), ADD)

  def get_attack_multiplier(self, damage_type):
    """Placeholder to be replaced when stat system is removed."""
    if damage_type == PHYSICAL:
      relevant_stat = self.attack
    elif damage_type == SPECIAL:
      relevant_stat = self.sp_attack
    else:
      raise ValueError('Invalid damage type %s' % damage_type)

    aura_effect = self.get_aura_effect((damage_type, ATTACK_MULTIPLIER), MULT)

    return aura_effect * STAT_EXPONENT_BASE ** relevant_stat

  def get_defense_multiplier(self, damage_type):
    """Placeholder to be replaced when stat system is removed."""
    if damage_type == PHYSICAL:
      relevant_stat = self.defense
    elif damage_type == SPECIAL:
      relevant_stat = self.sp_defense
    else:
      raise ValueError('Invalid damage type %s' % damage_type)

    aura_effect = self.get_aura_effect((damage_type, DEFENSE_MULTIPLIER), MULT)

    return aura_effect * STAT_EXPONENT_BASE ** -relevant_stat

  def get_damage_bonus(self, damage_type):
    return self.get_aura_effect((damage_type, FLAT_DAMAGE_BONUS), ADD)

  def get_def_bonus(self, damage_type):
    return self.get_aura_effect((damage_type, FLAT_DEFENSE_BONUS), ADD)

  def get_attack_damage_multiplier(self, damage_type):
    return self.get_aura_effect((damage_type, ATTACK_DAMAGE_MULTIPLIER), MULT)

  def get_defending_damage_multiplier(self, damage_type):
    return self.get_aura_effect((damage_type, DEFENDING_DAMAGE_MULTIPLIER), MULT)

  def take_turn(self, battle):
    raise NotImplementedError

  def decrement_auras(self):
    auras = []
    for aura in self.auras:
      aura.duration -= 1
      if aura.duration > 0:
        auras.append(aura)
      else:
        print('%s wore off' % aura.name)
    self.auras = auras

  def get_aura_effect(self, key, aggregation_method):
    if aggregation_method == ADD:
      effect = 0
    elif aggregation_method == MULT:
      effect = 1
    else:
      raise ValueError('Invalid aggregation method %s' % aggregation_method)
    for aura in self.auras:
      if aura.effects_dict[key] is not None:
        if aggregation_method == ADD:
          effect += aura.effects_dict[key]
        elif aggregation_method == MULT:
          effect *= aura.effects_dict[key]
    return effect


class Enemy(Actor):
  def take_turn(self, battle):
    target = random.choice(battle.players)
    self.attack_target(target)
    self.decrement_auras()

  def react(self, interactor):
    print("%s didn't like that" % self.name)

  def get_base_damage(self, damage_type):
    """Default behavior: deal basic physical and special damage."""
    return {
        PHYSICAL: 1,
        SPECIAL: 1,
    }[damage_type]


class PapaRoach(Enemy):
  def __init__(self):
    Enemy.__init__(
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
        PHYSICAL: 1,
        SPECIAL: 0,
    }[damage_type]


class LilBug(Enemy):
  def __init__(self, identifier):
      Enemy.__init__(
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
        PHYSICAL: 1,
        SPECIAL: 0,
    }[damage_type]

  def react(self, interactor):
    print("%s bit %s's finger. %s took 1 damage." %
          (self.name, interactor.name, interactor.name))
    interactor.take_damage(1)


class Player(Actor):
  def __init__(self, name, max_hp, attack, defense, sp_attack, sp_defense,
               speed, inventory, equipped=None):
    Actor.__init__(self, name, max_hp, attack, defense, sp_attack, sp_defense,
                   speed)
    self.inventory = inventory
    self.equipped = equipped

  def take_turn(self, battle):
    action_points = MAX_ACTION_POINTS
    while action_points:
      actions = [('attack', 3),
                 ('item', 1),
                 ('interact', 3),
                 ('end turn', 0),
                 ('look', 0)]
      action, cost = choose_option(actions)
      if cost > action_points:
        print('You only have %d AP' % action_points)
      else:
        action_points -= cost
        if action == 'attack':
          target = choose_option(battle.enemies)
          self.attack_target(target)
        elif action == 'item':
          if self.inventory:
            item = choose_option(self.inventory)
            valid_targets = item.get_valid_targets(self, battle)
            if valid_targets:
              target = choose_option(valid_targets)
              item.use(self, target)
            else:
              print('No valid targets')
              action_points += cost
          else:
            print('No items')
            action_points += cost
        elif action == 'interact':
          target = choose_option(battle.enemies)
          self.interact(target)
        elif action == 'end turn':
          action_points = 0
        elif action == 'look':
          battle.explain()

    self.decrement_auras()

  def get_base_damage(self, damage_type):
    if self.equipped is None:
      # Unarmed damage.
      return {
          PHYSICAL: 1,
          SPECIAL: 0,
      }[damage_type]
    else:
      return self.equipped.get_damage(damage_type)

  def interact(self, target):
    target.react(self)


class Aura():
  def __init__(self, name, effects_dict, duration=1):
    self.name = name
    self.effects_dict = collections.defaultdict(lambda: None, effects_dict)
    self.duration = duration

  def __repr__(self):
    return '%s (%d)' % (self.name, self.duration)

class Item():
  def get_valid_targets(self, user, battle):
    return battle.players + battle.enemies

  def use(self, user, target):
    user.inventory.remove(self)


class Potion(Item):
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
        (PHYSICAL, ATTACK_DAMAGE_MULTIPLIER): 1.25,
        (PHYSICAL, DEFENDING_DAMAGE_MULTIPLIER): 1.25,
        (SPECIAL, DEFENDING_DAMAGE_MULTIPLIER): 1.25,
    }, duration=3)
    user.auras.append(berserker_aura)
    user.inventory.remove(self)

  def __repr__(self):
    return 'Berserker Potion'

class Weapon(Item):
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
        PHYSICAL: self.base_power,
        SPECIAL: 0,
    }[damage_type]


class MagicWand(Weapon):
  """A basic deterministic special weapon."""
  def __init__(self, name, base_power):
    Weapon.__init__(self, name)
    self.base_power = base_power

  def get_damage(self, damage_type):
    return {
        PHYSICAL: 0,
        SPECIAL: self.base_power,
    }[damage_type]


class Battle():
  def __init__(self, players, enemies):
    self.players = players
    self.enemies = enemies

  def explain(self):
    player_infos = [(player.name, player.hp) for player in self.players]
    enemy_infos = [(enemy.name, enemy.hp) for enemy in self.enemies]

    print('players: ', player_infos)
    print('enemies: ', enemy_infos)

  def remove_dead_actors(self):
    self.players = [player for player in self.players if player.alive]
    self.enemies = [enemy for enemy in self.enemies if enemy.alive]
    self.initiative_order = [
        actor for actor in self.initiative_order if actor.alive
    ]

  def spawn_enemy(self, enemy, move_this_round=False):
    self.enemies.append(enemy)
    if move_this_round:
      self.sort_initiative_order(self.initiative_order + [enemy])

  def sort_initiative_order(self, actors):
    self.initiative_order = sorted(actors,
                                   key=lambda actor: (-actor.speed, actor.name))

  def run_round(self):
    self.sort_initiative_order(self.players + self.enemies)
    while self.initiative_order:
      print('========================================')
      current_actor = self.initiative_order.pop(0)
      current_actor.take_turn(self)
      self.remove_dead_actors()

  def run_turn(self):
    print('========================================')
    
    current_actor = self.initiative_order[self.current_actor_index]
    current_actor.take_turn(self)

    self.current_actor_index = (
        (self.current_actor_index + 1) % len(self.initiative_order))

  def start(self):
    while self.players and self.enemies:
      self.run_round()
    if not self.players:
      print('All players dead. You lose.')
    elif not self.enemies:
      print('All enemies dead. You win.')


def get_equipped_string(equipped):
  return equipped.name if equipped is not None else 'unarmed'


def choose_option(options):
  print('choices: ', list(enumerate(options)))
  choice = None
  while choice is None:
    try:
      choice = options[int(input())]
    except ValueError:
      print('invalid input.')
    except IndexError:
      print('invalid input.')
  return choice


def main():
  sword = Sword('Sword', 2)
  magic_wand = MagicWand('Magic wand', 2)
  anzacel = Player(
      name='Anzacel',
      max_hp=10,
      attack=10,
      defense=10,
      sp_attack=10,
      sp_defense=10,
      speed=10,
      inventory=[BerserkerPotion(), Potion(), sword, magic_wand])

  battle = Battle([anzacel], [PapaRoach()])
  battle.explain()
  battle.start()


if __name__ == '__main__':
  main()
