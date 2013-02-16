from django.utils import simplejson
import urllib
import logging
from domain import Business
from repository import Business_Repository
from google.appengine.ext import db

BASE_URL = 'http://api.sandbox.yellowapi.com'
API_KEY = '9k5g4bqucenr9ztnh9x693cw'
SEARCH_TERM = 'scrapbook'

class YellowpagesBusinessSearchService:         
	def getBusinessesByGeoLocation(self, latitude, longitude, clientIP):
		location = 'cZ' + str(longitude) + ',' + str(latitude)
		url = BASE_URL + '/FindBusiness/?what=' + SEARCH_TERM + '&where=' + location + '&fmt=JSON&pgLen=100&apikey=' + API_KEY + '&UID=' + clientIP
		logging.info("called simplejson.load " + url)
		result = simplejson.load(urllib.urlopen(url))
		return self.buildBusinessFromJson(result)		
    
	def getBusinessesByNameInCity(self, name, city, clientIP):
		# http://api.sandbox.yellowapi.com/FindBusiness/?what=scrapbook%20studio&where=saskatoon&fmt=JSON&pgLen=10&apikey=9k5g4bqucenr9ztnh9x693cw&UID=127.0.0.1
		encodedName = urllib.quote(name.encode("utf-8"))
		encodedCity = urllib.quote(city.encode("utf-8"))
		url = BASE_URL + '/FindBusiness/?what=' + encodedName + '&where=' + encodedCity + '&fmt=JSON&pgLen=100&apikey=' + API_KEY + '&UID=' + clientIP
		logging.info("called simplejson.load " + url)
		result = simplejson.load(urllib.urlopen(url))
		return self.buildBusinessFromJson(result)

	def getBusinessesByCity(self, city, clientIP):
		encodedCity = urllib.quote(city.encode("utf-8"))		
		url = BASE_URL + '/FindBusiness/?what=' + SEARCH_TERM + '&where=' + encodedCity + '&fmt=JSON&pgLen=100&apikey=' + API_KEY + '&UID=' + clientIP
		logging.info("called simplejson.load " + url)
		result = simplejson.load(urllib.urlopen(url))
		return self.buildBusinessFromJson(result)
		
	def getBusinessesByCityFile(self, city):
		encodedCity = urllib.quote(city.encode("utf-8"))		
		url = '/Users/Dean/Documents/Code/ScrapItServices/testJson.json'
		logging.info("called simplejson.load " + url)
		result = simplejson.load(open(url, 'r'))
		return self.buildBusinessFromJson(result)
		
	def getBusinessByIdWithNameInProvince(self, yellowpages_id, name, province, clientIP):
		#http://api.yellowapi.com/GetBusinessDetails/?prov=Saskatchewan&city=Saskatoon&bus-name=just-scrap-it&listingId=4436892fmt=XML&apikey=a1s2d3f4g5h6j7k8l9k6j5j4&UID=127.0.0.1	
		encodedProvince = urllib.quote(province.encode("utf-8"))
		encodedId = urllib.quote(yellowpages_id.encode("utf-8"))
		logging.info("name: " + name)
		encodedName = urllib.quote(name.encode("utf-8"))
		url = BASE_URL + '/GetBusinessDetails/?prov=' + encodedProvince + '&listingId=' + encodedId + '&bus-name=' + encodedName + '&fmt=JSON&pgLen=100&apikey=' + API_KEY + '&UID=' + clientIP
		logging.info("called simplejson.load " + url)
		result = simplejson.load(urllib.urlopen(url))
		return self.buildBusinessDetailsFromJson(result)
		
	def buildBusinessFromJson(self, json):	
		businesses = []	
		if 'listings' in json:
			listings = json['listings']		
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
		
	def buildBusinessDetailsFromJson(self, json):	
		if 'id' in json:	
			business = Business()
			business.yellowpages_id = json['id']
			business.name = json['name']
			if 'address' in json:
				if json['address']:
					address = json['address']
					business.city = address['city']
					business.province = address['prov']
					business.country = 'Canada'
					business.street = address['street']
			if 'geoCode' in json:
				if json['geoCode']:
					geolocation = json['geoCode']
					lat = geolocation['latitude']
					lon = geolocation['longitude']
					business.geolocation = str(lat) + ', ' + str(lon)
			if 'phones' in json:
				if json['phones']:
					phones = json['phones']
					for phone in phones:
						if 'type' in phone:
							phoneType = phone['type']
							if phoneType == 'primary':
								business.phonenumber = phone['dispNum']
			if 'merchantUrl' in json:
				if json['merchantUrl']:
					url = json['merchantUrl']
					business.url = url
			return business
		else:
			return None

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
		
	def getBusinessesByNameInCity(self, name, city, clientIP):
		if not name:
			yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByCity(city, clientIP)
		else:
			yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByNameInCity(name, city, cientIP)
		return self.combineBusinesses(yellowpages_businesses)
	
	def getBusinessesByGeoLocation(self, latitude, longitude, clientIP):
		yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByGeoLocation(latitude, longitude, clientIP)
		return self.combineBusinesses(yellowpages_businesses)
		
	def getBusinessByDetails(self, yellowpages_id, name, provice, clientIP):
		yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessByIdWithNameInProvince(yellowpages_id, name, provice, clientIP)
		return self.combineBusiness(yellowpages_businesses)
		
	def combineBusinesses(self, yellowpages_businesses):
		combined_businesses = []
		for business in yellowpages_businesses:
			combinedBusiness = self.combineBusiness(business)
			combined_businesses.append(combinedBusiness)
		return combined_businesses
		
	def combineBusiness(self, business):
		repo_business = Business_Repository().getBusinessByYellowPagesId(business.yellowpages_id)
		if repo_business:
			business.url = repo_business.url
		return business

class JsonService:
	def getJsonForBusinessWithYellowPagesId(self, yellowpages_id):
		business = BusinessService().getBusinessByYellowPagesId(yellowpages_id)
		return BusinessEncoder().encode(business)
		
	def getJsonForBusinessesInCity(self, city, clientIP):
		businesses = BusinessService().getBusinessesByNameInCity('',city, clientIP)
		return self.encodeBusinesses(businesses)
		
	def getJsonForBusinessesInGeoLocation(self, latitude, longitude, clientIP):
		businesses = BusinessService().getBusinessesByGeoLocation(latitude, longitude, clientIP)
		return self.encodeBusinesses(businesses)
	
	def getJsonForBusinessWithDetails(self, yellowpages_id, province, name, clientIP):
		business = BusinessService().getBusinessByDetails(yellowpages_id, name, province, clientIP)
		return BusinessEncoder().encode(business)
	
	def encodeBusinesses(self, businesses):
		jsonData = []
		for business in businesses:
			encodedBusiness = BusinessEncoder().encode(business)
			jsonData.append(simplejson.loads(encodedBusiness))
		jsonBusinesses = JsonListEncoder().encode(jsonData)
		return '{ "items": ' + jsonBusinesses + '}'
		
class BusinessEncoder(simplejson.JSONEncoder):
	# json serialization example: http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
	def default(self, business):
		if not isinstance (business, Business):
			print 'You cannot use the JSON custom MyClassEncoder for a non-MyClass object.'
			return
		geolocationString = None
		if business.geolocation:
			geolocationString = {'latitude': business.geolocation.lat, 'longitude': business.geolocation.lon }
		return {'url': business.url, 'yellowpages_id': business.yellowpages_id, 'name': business.name, 'address': {'province': business.province
		, 'country': business.country, 'city': business.city, 'street': business.street}, 'phoneNumber': business.phonenumber, 'geoCode': geolocationString }
		
class JsonListEncoder(simplejson.JSONEncoder):
	def default(self, o):
		try:
			iterable = iter(o)
		except TypeError:
			pass
		else:
			return list(iterable)
		return JSONEncoder.default(self, o)