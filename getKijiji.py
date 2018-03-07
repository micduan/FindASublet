from urllib2 import urlopen as uReq
from urlparse import urlparse
from bs4 import BeautifulSoup as soup
import sys
import sqlite3
import re

def generateListings(bedrooms, furnished):

	my_other_url = 'https://www.kijiji.ca/b-short-term-rental/gta-greater-toronto-area/sublet/k0c42l1700272'

	index = my_other_url.find('/sublet/') + len('/sublet/')
	url_end = my_other_url[index:]

	if (bedrooms == '1'):
		url_end = '1+bedroom/' + url_end
	elif (bedrooms == '2'):
		url_end = '2+bedrooms/' + url_end
	elif (bedrooms == '3'):
		url_end = '3+bedrooms/' + url_end
	elif (bedrooms == '4'):
		url_end = '4+bedrooms__5+bedrooms__6+more+bedrooms' + url_end

	if (furnished == 'Y'):
		url_end = url_end + '?furnished=1'
	elif (furnished == 'N'):
		url_end = url_end + '?furnished=0'

	my_url = my_other_url[:index] + url_end

	uClient = uReq(my_url)

	page_html = uClient.read()

	uClient.close()
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll(True, {"class": ['search-item', 'regular-ad']})

	return containers

def getMonths(ad):
	months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan ', 'feb ', 'mar ', 'apr ', 'aug ', 'sept ', 'oct ', 'nov ', 'dec ']
	matched_months = []

	title = ad.find('div', {"class" : "title"}).text
	location = ad.find('div', {"class" : "description"}).text

	for month in months:
		if (re.search(month, title, re.IGNORECASE) or re.search(month, location, re.IGNORECASE)):
			if not re.search(month + ".*", ' '.join(matched_months)):
				matched_months.append(month)

	return matched_months

def getIntersection(ad):
	streets = ['Gerrard', 'Church', 'Yonge', 'Finch']
	slash_indices = [m.start() for m in re.finditer('/', ad.find('div', {"class" : "title"}).text)]
	and_indices = [m.start() for m in re.finditer('and', ad.find('div', {"class" : "title"}).text)]
	intersection = []

	for index in slash_indices + and_indices:
		starting = ad.find('div', {"class" : "title"}).text[:index]
		ending = ad.find('div', {"class" : "title"}).text[index:]

		for street in streets:
			if (re.search(street, starting, re.IGNORECASE)):
				intersection.append(street)

		for street in streets:
			if (re.search(street, ending, re.IGNORECASE)):
				intersection.append(street)	

	return intersection

def sqlite_insert(conn, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()

def saveListings():

	data = []
	kijiji = generateListings(request.form['bedrooms'], request.form['furnished'])

	sqlite_file='db.sqlite'
	table_name='kijiji'
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	for listing in kijiji:
		dict = {}
		dict['link'] = "https://www.kijiji.ca" + listing.find('div', {"class" : "title"}).a['href']
		dict['title'] = listing.find('div', {"class" : "title"}).text
		dict['price'] = listing.find('div', {"class" : "price"}).text

		intersection = getKijiji.getIntersection(listing)

		if intersection and len(intersection) > 0:
			if len(intersection) > 1:
				dict['intersection2'] = intersection[1]
			dict['intersection1'] = intersection[0]

		dates = getKijiji.getMonths(listing)
		dict['start_date'] = ''
		dict['end_date'] = ''

		if len(dates) > 0:
			dict['start_date'] = dates[0].title()
		if len(dates) > 1:
			dict['end_date'] = dates[-1].title()

		dict['other'] = 'kijiji'

		sqlite_insert(conn, 'kijiji', dict)










