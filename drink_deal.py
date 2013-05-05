class DrinkDeal:

  # Days
  SUNDAY = 0
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6

  #Categories
  BEER = 0
  WINE = 1
  SPIRIT = 2

  def __init__(self, data):
    self.day = data['day']
    self.drink_name = data['drink_name']
    self.drink_