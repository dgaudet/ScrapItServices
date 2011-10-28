from django.utils import simplejson
import urllib
import logging
from domain import Business
from repository import Business_Repository
from google.appengine.ext import db

BASE_URL = 'http://api.sandbox.yellowapi.com'
API_KEY = '9k5g4bqucenr9ztnh9x693cw'

class YellowpagesBusinessSearchService:
	def getBusinessesByNameInCity(self, name, city):
		# http://api.sandbox.yellowapi.com/FindBusiness/?what=scrapbook%20studio&where=saskatoon&fmt=JSON&pgLen=10&apikey=9k5g4bqucenr9ztnh9x693cw&UID=127.0.0.1
		encodedName = urllib.quote(name)
		encodedCity = urllib.quote(city)
		businesses = []
		url = BASE_URL + '/FindBusiness/?what=' + encodedName + '&where=' + encodedCity + '&fmt=JSON&pgLen=10&apikey=' + API_KEY + '&UID=127.0.0.1'
		logging.info("called simplejson.load " + url)
		result = simplejson.load(urllib.urlopen(url))
		if 'listings' in result:
			listings = result['listings']		
			for listing in listings:
				business = Business()
				business.yellowpages_id = listing['id']
				business.name = listing['name']
				if 'address' in listing:
					if listing['address']:
						address = listing['address']
						business.city = address['city']
						business.province = address['prov']
						business.country = 'Canada'
						business.street = address['street']
				if 'geoCode' in listing:
					if listing['geoCode']:
						geolocation = listing['geoCode']
						lat = geolocation['latitude']
						lon = geolocation['longitude']
						business.geolocation = str(lat) + ', ' + str(lon)
				businesses.append(business)
		return businesses

class BusinessService:
	def updateBusinessUrl(self, yellowpages_id, url):
		business = Business()
		business.yellowpages_id = yellowpages_id
		business.url = url
		Business_Repository().save(business)
	
	def getBusinesses(self):
		businesses = Business_Repository().getAllBusinesses()
		for business in businesses:
			logging.info('id: ' + business.yellowpages_id + ' url: ' + business.url)
		return businesses
		
	def getBusinessByYellowPagesId(self, yellowpages_id):
		return Business_Repository().getBusinessByYellowPagesId(yellowpages_id)
		
	def getBusinessesByNameInCity(self, name, city):
		yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByNameInCity(name, city)
		combined_businesses = []
		for business in yellowpages_businesses:
			repo_business = Business_Repository().getBusinessByYellowPagesId(business.yellowpages_id)
			if repo_business:
				business.url = repo_business.url
			combined_businesses.append(business)
		return combined_businesses

class JsonService:
	def getJsonForBusinessWithYellowPagesId(self, yellowpages_id):
		business = BusinessService().getBusinessByYellowPagesId(yellowpages_id)
		return BusinessEncoder().encode(business)
		
class BusinessEncoder(simplejson.JSONEncoder):
	# json serialization example: http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
	def default(self, business):
		if not isinstance (business, Business):
			print 'You cannot use the JSON custom MyClassEncoder for a non-MyClass object.'
			return
		return {'url': business.url, 'yellowpages_id': business.yellowpages_id}