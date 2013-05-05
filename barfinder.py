# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
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
  drink_deals = DrinkDeal.all_deals(g.db)
  return render_template('show_drink_deals.html', drink_deals=drink_deals)

@app.route('/add_drink_deal', methods=['POST'])
def add_drink_deal():
  deal = DrinkDeal((request.form['day'], request.form['drink_cost'], request.form['drink_name'], request.form['drink_category'], request.form['bar_name'], request.form['bar_lat'], request.form['bar_lon']))
  deal.save(g.db)
  flash('New bar was created')
  return redirect(url_for('show_drink_deals'))

@app.route('/show_map', methods=['GET'])
def show_map():
  return render_template('map.html')

@app.route('/get_drinks_json', methods=['GET'])
def drink_json_data():
  data = []
  for deal in DrinkDeal.all_deals(g.db):
    data.append(deal.to_arr())
  return jsonify([('json-data',data)])

if __name__ == '__main__':
  app.run()