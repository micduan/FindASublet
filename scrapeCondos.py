from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import re

my_url = 'https://www.kijiji.ca/b-short-term-rental/gta-greater-toronto-area/sublet/1+bathroom/k0c42l1700272a26'

if len(sys.argv) > 1:
	my_url = sys.argv[1]

uClient = uReq(my_url)

page_html = uClient.read()

uClient.close()
page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll(True, {"class": ['search-item', 'regular-ad']})

for container in containers:
	print "Price" + container.find('div', {"class" : "price"}).text




