import battle_engine


class Heal(battle_engine.Ability):
  def __init__(self, amount, ap_cost=1):
    battle_engine.Ability.__init__(self, 'Heal', ap_cost)
    self.amount = amount

  def use(self, user, battle):
    user.heal(self.amount)