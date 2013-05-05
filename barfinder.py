# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from drink_deal import DrinkDeal

app = Flask(__name__)
app.config.from_object('configuration')

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  g.db.close()

@app.route('/')
def show_drink_deals():
  cur = g.db.execute('select name from bars order by id desc')
  bars = [row[0] for row in cur.fetchall()]
  return render_template('show_bars.html', bars=bars)

@app.route('/add_drink_deal', methods=['POST'])
def add_drink_deal():
  g.db.execute('insert into bars (name, latitude, longitude) values (?, ?, ?)',
                [request.form['name'], request.form['latitude'], request.form['longitude']])
  g.db.commit()
  flash('New bar was created')
  return redirect(url_for('show_bars'))

if __name__ == '__main__':
  app.run()