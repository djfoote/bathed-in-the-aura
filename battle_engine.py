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

# Stats
POWER = 'power'
STRENGTH = 'strength'
RESISTANCE = 'resistance'
ARMOR = 'armor'

# Non-stat damage quantities
DAMAGE_BONUS = 'damage_bonus'
DAMAGE_MULTIPLIER = 'damage_multiplier'
RECEIVED_DAMAGE_MULTIPLIER = 'receieved_damage_multiplier'

# Aggregation methods
ADD = 'add'
MULT = 'mult'


class Actor():
  def __init__(self, name, max_hp, stat_dict, speed, auras=None):
    self.name = name

    self.max_hp = max_hp
    self.hp = max_hp
    self.alive = True

    self.stats = stat_dict

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

  def attack_target(self, target, attack_tags):
    phys_damage = self.get_attack_damage(target, PHYSICAL, attack_tags)
    sp_damage = self.get_attack_damage(target, SPECIAL, attack_tags)
    crit = random.random() < CRIT_PROBABILITY
    crit_multiplier = CRIT_MULTIPLIER if crit else 1

    damage = round((phys_damage + sp_damage) * crit_multiplier)

    print('%s attacked %s.' % (self.name, target.name))
    if crit:
      print('Critical hit!')
    print('%s took %d damage.' % (target.name, damage))

    target.take_damage(damage)
    target.respond_to_attack(self)

  def get_attack_damage(self, target, damage_type, attack_tags=()):
    base_damage = self.get_base_damage(damage_type)

    if damage_type in attack_tags:
      # Only add user's power if weapon deals corresponding damage type.
      base_damage += self.get_power(damage_type)

    attack_mult = self.get_strength(damage_type)
    def_mult = target.get_resistance(damage_type)
    damage_bonus = self.get_damage_bonus(damage_type)
    def_bonus = target.get_armor(damage_type)
    atk_damage_mult = self.get_damage_multiplier(damage_type)
    def_damage_mult = target.get_received_damage_multiplier(damage_type)

    return compute_damage(
        base_damage, attack_mult, def_mult, damage_bonus, def_bonus,
        atk_damage_mult, def_damage_mult)

  def get_base_damage(self, damage_type):
    raise NotImplementedError

  def get_power(self, damage_type):
    stat = self.stats[(damage_type, POWER)]
    aura_effect = self.get_aura_effect((damage_type, POWER), ADD)
    return stat + aura_effect

  def get_strength(self, damage_type):
    stat = self.stats[(damage_type, STRENGTH)]
    aura_effect = self.get_aura_effect((damage_type, STRENGTH), MULT)
    return stat * aura_effect

  def get_resistance(self, damage_type):
    stat = self.stats[(damage_type, RESISTANCE)]
    aura_effect = self.get_aura_effect((damage_type, RESISTANCE), MULT)
    return stat * aura_effect

  def get_damage_bonus(self, damage_type):
    return self.get_aura_effect((damage_type, DAMAGE_BONUS), ADD)

  def get_armor(self, damage_type):
    stat = self.stats[(damage_type, ARMOR)]
    aura_effect = self.get_aura_effect((damage_type, ARMOR), ADD)
    return stat + aura_effect

  def get_damage_multiplier(self, damage_type):
    return self.get_aura_effect((damage_type, DAMAGE_MULTIPLIER), MULT)

  def get_received_damage_multiplier(self, damage_type):
    return self.get_aura_effect((damage_type, RECEIVED_DAMAGE_MULTIPLIER), MULT)

  def take_turn(self, battle):
    raise NotImplementedError

  def respond_to_attack(self, attacker):
    pass

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
    self.attack_target(target, self.get_standard_attack_tags())
    self.decrement_auras()

  def is_interactable(self):
    return False

  def react(self, interactor):
    raise NotImplementedError

  def get_base_damage(self, damage_type):
    """Default behavior: deal basic physical and special damage."""
    return {
        PHYSICAL: 1,
        SPECIAL: 1,
    }[damage_type]

  def get_standard_attack_tags(self):
    return [PHYSICAL, SPECIAL]


class Player(Actor):
  def __init__(self, name, max_hp, stat_dict, speed, inventory, equipped=None):
    Actor.__init__(self, name, max_hp, stat_dict, speed)
    self.inventory = inventory
    self.equipped = equipped

  def get_available_actions(self, battle, action_points):
    all_actions = [('attack', 3),
                   ('item', 1),
                   ('interact', 3),
                   ('end turn', 0),
                   ('look', 0)]
    available_actions = []
    for action, cost in all_actions:
      if cost > action_points:
        continue
      elif action == 'item':
        if self.inventory:
          available_actions.append((action, cost))
      elif action == 'interact':
        if self.get_interaction_targets(battle):
          available_actions.append((action, cost))
      else:
        available_actions.append((action, cost))
    return available_actions


  def take_turn(self, battle):
    action_points = MAX_ACTION_POINTS
    while action_points:
      actions = self.get_available_actions(battle, action_points)
      action, cost = choose_option(actions)
      if cost > action_points:
        print('You only have %d AP' % action_points)
      else:
        action_points -= cost
        if action == 'attack':
          target = choose_option(battle.enemies)
          self.attack_target(target, self.get_attack_tags())
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

  def get_attack_tags(self):
    if self.equipped:
      return self.equipped.tags
    else:
      # Unarmed.
      return [PHYSICAL]

  def interact(self, target):
    target.react(self)

  def get_interaction_targets(self, battle):
    return [enemy for enemy in battle.enemies if enemy.is_interactable()]


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
      print("%s's turn" % current_actor)
      current_actor.take_turn(self)
      self.remove_dead_actors()

  def start(self):
    while self.players and self.enemies:
      self.run_round()
    if not self.players:
      print('All players dead. You lose.')
    elif not self.enemies:
      print('All enemies dead. You win.')


def compute_damage(power, strength, resistance, damage_bonus, armor,
                   damage_mult, receieved_damage_mult):
  raw_damage = power * strength / resistance + damage_bonus - armor
  return max(0, raw_damage) * damage_mult * receieved_damage_mult


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
