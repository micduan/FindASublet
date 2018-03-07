from urllib2 import urlopen as uReq
from urlparse import urlparse
from bs4 import BeautifulSoup as soup
import sys
import sqlite3
import getKijiji
import re

def generateListings(bedrooms, furnished):

	my_other_url = 'https://toronto.craigslist.ca/search/sub'

	uClient = uReq(my_other_url)

	page_html = uClient.read()

	uClient.close()
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll(True, {"class": ['result-row']})
	return containers

def getIntersection(ad):
	streets = ['Gerrard', 'Church', 'Yonge', 'Finch', 'Junction', 'Triangle', 'Queens Quay West', 'Spadina', 'Olive', 'Queens', 'Portland', 'Sheppard', 'Dufferin', 'St Clair', 'Front', 'Bathurst']

	result_text = ad.find(True, {"class" : "result-hood"})

	if not result_text:
		return []

	index = result_text.find('/')
	index2 = result_text.find('and')
	intersection = []


	for index in [index, index2]:
		starting = ad.find(True, {"class" : "result-hood"}).text[:index]
		ending = ad.find(True, {"class" : "result-hood"}).text[index:]

		for street in streets:
			if (re.search(street, starting, re.IGNORECASE)):
				intersection.append(street)

		for street in streets:
			if (re.search(street, ending, re.IGNORECASE)):
				intersection.append(street)	

	return intersection

def getMonths(ad):
	months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan ', 'feb ', 'mar ', 'apr ', 'aug ', 'sept ', 'oct ', 'nov ', 'dec ']
	matched_months = []

	title = ad.find(True, {"class" : "result-title"})
	if title:
		title = title.text
	else:
		title = ''
	result_hood = ad.find(True, {"class" : "result-hood"})
	if result_hood:
		result_hood = result_hood.text
	else:
		result_hood = ''
	housing = ad.find(True, {"class" : "housing"})
	if housing:
		housing = housing.text
	else:
		housing = ''

	for month in months:
		if (re.search(month, title, re.IGNORECASE) or re.search(month, result_hood, re.IGNORECASE) or re.search(month, housing, re.IGNORECASE)):
			if not re.search(month + ".*", ' '.join(matched_months)):
				matched_months.append(month)

	return matched_months

def getBedrooms(ad):
	housing = ad.find(True, {"class" : "housing"})
	if housing:
		housing = housing.text
	else:
		housing = ''

	expression = re.search('\d+\s?br*', housing)
	if expression:
		index = expression.start()
		return housing[index]
	return ''

def saveListings():
	data = []
	listings = generateListings(0, 0)

	sqlite_file='db.sqlite'
	table_name='kijiji'
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	for listing in listings:
		dict = {}
		price = listing.find(True, {"class" : "result-price"})
		if price:
			dict['price'] = price.text

		title = listing.find(True, {"class" : ['result-title', 'hdrlnk']})
		if title:
			dict['title'] = title.text

		dict['other'] = 'craigslist'

		intersection = getIntersection(listing)

		if intersection and len(intersection) > 0:
			if len(intersection) > 1:
				dict['intersection2'] = intersection[1]
			dict['intersection1'] = intersection[0]

		dates = getMonths(listing)

		if len(dates) > 0:
			dict['start_date'] = dates[0].title()
		if len(dates) > 1:
			dict['end_date'] = dates[-1].title()

		dict['bedrooms'] = getBedrooms(listing)

		getKijiji.sqlite_insert(conn, 'kijiji', dict)

		data.append(dict)
	return data

def addLinkToDB():
	listings = generateListings(0, 0)
	sqlite_file='db.sqlite'
	table_name='kijiji'
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	for listing in listings:
		title = listing.find(True, {"class" : ['result-title', 'hdrlnk']})
		if title:
			title = title.text
		else:
			continue

		c.execute('SELECT * FROM kijiji WHERE other="craigslist"')


		return c


		url = listing.find(True, {"class" : ['result-title', 'hdrlnk']})
		if url:
			url = url['href']

	return 'done'


