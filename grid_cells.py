class GridCell():
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.name


class AddStats(GridCell):
  def __init__(self, name, stats_dict):
    GridCell.__init__(self, name)
    self.stats_dict = stats_dict


class MultiplyStats(GridCell):
  def __init__(self, name, stats_dict):
    GridCell.__init__(self, name)
    self.stats_dict = stats_dict


class AddPraySpells(GridCell):
  def __init__(self, name, spells):
    GridCell.__init__(self, name)
    self.spells = spells


class IncreaseNumberOfPrayOptions(GridCell):
  def __init__(self, name, amount):
    GridCell.__init__(self, name)
    self.amount = amount