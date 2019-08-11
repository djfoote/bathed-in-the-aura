import random

MAX_ACTION_POINTS = 3


class Actor():
  def __init__(self, name, max_hp, attack, defense, sp_attack, sp_defense,
               speed):
    self.name = name

    self.max_hp = max_hp
    self.hp = max_hp
    self.alive = True

    self.attack = attack
    self.defense = defense
    self.sp_attack = sp_attack
    self.sp_defense = sp_defense
    self.speed = speed

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
    damage = max(0, self.attack - target.defense)
    print('%s attacked %s for %d damage.' % (self.name, target.name, damage))
    target.take_damage(damage)

  def take_turn(self, battle):
    raise NotImplementedError

  def interact(self, target):
    target.react(self)

  def react(self, interactor):
    raise NotImplementedError


class Enemy(Actor):
  def take_turn(self, battle):
    target = random.choice(battle.players)
    self.attack_target(target)

  def react(self, interactor):
    print("%s didn't like that" % self.name)


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

  def attack_target(self, target):
    if self.equipped:
      special = self.equipped.special
      damage_bonus = self.equipped.get_damage()
    else:
      special = False
      damage_bonus = 0
    if special:
      damage = self.sp_attack - target.sp_defense + damage_bonus
    else:
      damage = self.attack - target.defense + damage_bonus
    damage = max(0, damage)
    print('%s attacked %s with %s for %d damage.' % (
        self.name, target.name, get_equipped_string(self.equipped), damage))
    target.take_damage(damage)


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


class Weapon():
  def __init__(self, name, damage_range, special):
    self.name = name

    # Damage range is doubly inclusive.
    self.damage_range = damage_range
    self.special = special

  def get_damage(self):
    return random.randint(*self.damage_range)

  def get_valid_targets(self, user, battle):
    return [user]

  def use(self, user, target):
    print('%s equipped' % self.name)
    user.equipped = self

  def __repr__(self):
    return '%s %s %s' % (self.name, self.damage_range,
                         get_special_string(self.special))


class Battle():
  def __init__(self, players, enemies):
    self.players = players
    self.enemies = enemies

    self.init_initiative_order()
    self.current_actor_index = 0

  def explain(self):
    player_infos = [(player.name, player.hp) for player in self.players]
    enemy_infos = [(enemy.name, enemy.hp) for enemy in self.enemies]

    print('players: ', player_infos)
    print('enemies: ', enemy_infos)

  def remove_dead_actors(self):
    self.players = []
    self.enemies = []
    for i, actor in enumerate(self.initiative_order):
      if actor.alive:
        if isinstance(actor, Player):
          self.players.append(actor)
        if isinstance(actor, Enemy):
          self.enemies.append(actor)
      # Don't skip a turn when someone dies.
      elif i <= self.current_actor_index:
        self.current_actor_index -= 1

  def init_initiative_order(self):
    actors = self.players + self.enemies
    self.initiative_order = sorted(actors,
                                   key=lambda actor: (-actor.speed, actor.name))

  def run_turn(self):
    
    current_actor = self.initiative_order[self.current_actor_index]
    current_actor.take_turn(self)

    self.current_actor_index = (
        (self.current_actor_index + 1) % len(self.initiative_order))
    print(self.current_actor_index)

  def start(self):
    while self.players and self.enemies:
      self.run_turn()
      self.remove_dead_actors()
      # TODO: figure out logic for speed changes mid-match
      # Need to re-init initiative order at least every time someone dies.
      self.init_initiative_order()
    if not self.players:
      print('All players dead. You lose.')
    elif not self.enemies:
      print('All enemies dead. You win.')


def get_special_string(special):
  return 'Special' if special else 'Physical'


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
  sword = Weapon('Sword', (1, 3), False)
  staff = Weapon('Lightning staff', (1, 3), True)
  anzacel = Player(
      name='Anzacel',
      max_hp=10,
      attack=10,
      defense=10,
      sp_attack=10,
      sp_defense=10,
      speed=10,
      inventory=[Potion(), sword, staff])

  lil_bugs = [LilBug(i) for i in range(4)]
  lil_bugs[0].speed = 11

  battle = Battle([anzacel], lil_bugs)
  battle.explain()
  battle.start()


if __name__ == '__main__':
  main()
