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

  def __init__(self, data, my_id=-1):
    print "I hate you"
    self.id = my_id
    self.day = int(data[0])
    self.drink_cost = float(data[1])
    self.drink_name = data[2]
    self.drink_category = int(data[3])
    self.bar_name = data[4]
    self.bar_lat = float(data[5])
    print "here"
    self.bar_lon = float(data[6])
    print "goodbye"

  def save(self, db):
    db.execute('insert into drink_deals (day, drink_cost, drink_name, drink_category, bar_name, bar_lat, bar_lon) values (?, ?, ?, ?, ?, ?, ?)',
              [self.day, self.drink_cost, self.drink_name, self.drink_category, self.bar_name, self.bar_lat, self.bar_lon])
    db.commit()

  def delete(self, db):
    if self.id == -1:
      return
    db.execute('delete from drink_deals where id=?', [self.id])


  @staticmethod
  def all_deals(db):
    deals = []
    rows = db.execute('select * from drink_deals').fetchall()
    for row in rows:
      deals.append(DrinkDeal(row[1:], row[0]))
    return deals