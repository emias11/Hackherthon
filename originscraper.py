from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import regex as re
import requests
import pprint
#from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def getkilocandorigin(food):

	options = Options()
	options.headless = True
	options.add_argument("--enable-javascript")
	#options.add_argument("--window-size=1920,1200")

	driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')

	#get user input request
	user_input = food
	serialised_user_input = quote(user_input)
	driver.get(f"https://www.sainsburys.co.uk/gol-ui/SearchDisplayView?filters[keyword]={serialised_user_input}")
	time.sleep(5)
	links = driver.find_elements_by_tag_name('a')
	product_links = []
	for link in links:
		if "product/details/" in str(link.get_attribute("href")):
			product_links.append(link)

	item_link = product_links[0].get_attribute('href')
	driver.get(item_link)
	texts = []
	while len(texts) < 3:
		texts = driver.find_elements_by_class_name('productText')
		time.sleep(1)

	standard_texts = []
	for text in texts:
		standard_texts.append(text.text)

	nutrientslist = standard_texts[1].split("\n")
	energyinfo = nutrientslist[2]
	energyinfolist = energyinfo.split()
	energynums = []
	for energyi in energyinfolist:
		energyi = re.sub(r"[^0-9]", "", energyi)
		if energyi:
			energynums.append(int(energyi))
	kilocalories = max(energynums)

	growntext = texts[2].text
	if "," in growntext:
		head, sep, tail = growntext.partition(", ")
		growntext = head

	head, sep, tail = growntext.partition("in ")
	growntext = tail

	origincountry = growntext

	driver.quit()

	return kilocalories, origincountry


def get_latlong(searchkey):
	'''
	Finds latitude and longitude for input search term, and returns them in a tuple
	In:
	searchkey: string
	Out:
	tuple(float, float)
	'''
	geolocator = Nominatim(user_agent="hackherthon_A")
	location = geolocator.geocode(searchkey)
	return location.latitude, location.longitude


def get_distance(consumer,product_origin, unit='km'):
	'''
	Calculates distance between consumer and product country of origin
	In:
	consumer: string
	product_origin: string
	Out:
	dist: float
	'''
	consumer = get_latlong(consumer)
	product_origin = get_latlong(product_origin)

	if unit == 'miles':
		dist = geodesic(consumer,product_origin).miles
	if unit == 'km':
		dist = geodesic(consumer,product_origin).kilometers

	return dist


def get_fuel(origincountry):
	consumer_location = 'London'
	product_origin_location = origincountry
	dist= get_distance(consumer_location, product_origin_location, unit='km')
	fuel_used = dist * 12
	return fuel_used


def main(weight, food):
	kilocalories, origincountry = getkilocandorigin(food)
	fuel_used = get_fuel(origincountry)
	return kilocalories, fuel_used





