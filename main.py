from flask import Flask, render_template, request
from urlparse import urlparse
import getKijiji
import getCraigslist
import re
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/filter', methods=['POST'])
def filter():
	return render_template("filter.html", city=request.form['city'])

@app.route('/city', methods=['POST'])
def city():
	sqlite_file='db.sqlite'
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()
	if (request.form['bedrooms']):
		c.execute('SELECT * FROM kijiji WHERE bedrooms={my_id}'.\
		format(my_id=request.form['bedrooms']))
	else:
		c.execute('SELECT * FROM kijiji ')
	all_rows = c.fetchall()
	return render_template('city.html', test=all_rows, kijiji=[request.form['city']])

@app.route('/generateCraigslist', methods=['POST', 'GET'])
def craigslist():
	listings = getCraigslist.addLinkToDB()
	return render_template('city.html', test=listings, kijiji='hi')
	


if __name__ == "__main__":
    app.run(debug=True)