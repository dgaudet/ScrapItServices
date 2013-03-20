import json
import urllib
import logging
from domain import Business, GeoLocation
from repository import Yellow_Pages_Business_Repository, Yellowpages_Business, Business_Model_Repository, Business_Model
from appsettings import AppSettingsService

class YellowpagesBusinessSearchService:
	BASE_URL = AppSettingsService().yellowPagesBaseUrl()
	API_KEY = AppSettingsService().yellowPagesApiKey()
	SEARCH_TERM = 'scrapbook'
	ID_PREFIX = 'yellowPagesId:'
	
	def getBusinessesByGeoLocation(self, latitude, longitude):
		location = 'cZ' + str(longitude) + ',' + str(latitude)
		url = self.BASE_URL + '/FindBusiness/?what=' + self.SEARCH_TERM + '&where=' + location + '&fmt=JSON&pgLen=100'
		url = self.addRequiredParamsToUrl(url)
		logging.info("called json.load " + url)
		result = json.load(urllib.urlopen(url))
		return self.buildBusinessFromJson(result)		
    
	def getBusinessesByNameInCity(self, name, city):
		# http://api.sandbox.yellowapi.com/FindBusiness/?what=scrapbook%20studio&where=saskatoon&fmt=JSON&pgLen=10&apikey=9k5g4bqucenr9ztnh9x693cw&UID=127.0.0.1
		encodedName = urllib.quote(name.encode("utf-8"))
		encodedCity = urllib.quote(city.encode("utf-8"))
		url = self.BASE_URL + '/FindBusiness/?what=' + encodedName + '&where=' + encodedCity + '&fmt=JSON&pgLen=100'
		url = self.addRequiredParamsToUrl(url)
		logging.info("called json.load " + url)
		result = json.load(urllib.urlopen(url))
		return self.buildBusinessFromJson(result)

	def getBusinessesByCity(self, city):
		encodedCity = urllib.quote(city.encode("utf-8"))
		url = self.BASE_URL + '/FindBusiness/?what=' + self.SEARCH_TERM + '&where=' + encodedCity + '&fmt=JSON&pgLen=100'
		url = self.addRequiredParamsToUrl(url)
		logging.info("called json.load " + url)
		result = json.load(urllib.urlopen(url))
		return self.buildBusinessFromJson(result)
		
	def getBusinessesByCityFile(self, city):
		encodedCity = urllib.quote(city.encode("utf-8"))		
		url = '/Users/Dean/Documents/Code/ScrapItServices/testJson.json'
		logging.info("called json.load " + url)
		result = json.load(open(url, 'r'))
		return self.buildBusinessFromJson(result)
		
	def getBusinessByIdWithNameInProvince(self, yellowpages_id, name, province):
		#http://api.yellowapi.com/GetBusinessDetails/?prov=Saskatchewan&city=Saskatoon&bus-name=just-scrap-it&listingId=4436892fmt=XML&apikey=a1s2d3f4g5h6j7k8l9k6j5j4&UID=127.0.0.1	
		encodedProvince = urllib.quote(province.encode("utf-8"))
		idWithoutPrefix = Business().removePrefixFromId(yellowpages_id)
		encodedId = urllib.quote(idWithoutPrefix.encode("utf-8"))
		encodedName = urllib.quote(name.encode("utf-8"))
		url = self.BASE_URL + '/GetBusinessDetails/?prov=' + encodedProvince + '&listingId=' + encodedId + '&bus-name=' + encodedName + '&fmt=JSON&pgLen=100'
		url = self.addRequiredParamsToUrl(url)
		logging.info("called json.load " + url)
		result = json.load(urllib.urlopen(url))
		return self.buildBusinessDetailsFromJson(result)
		
	def buildBusinessFromJson(self, json):	
		businesses = []	
		if 'listings' in json:
			listings = json['listings']		
			for listing in listings:
				business = Business()
				business.business_id = business.formatYellowPagesId(listing['id'])
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
						business.geolocation = GeoLocation(lat, lon)
				businesses.append(business)
		return businesses
		
	def buildBusinessDetailsFromJson(self, json):	
		if 'id' in json:	
			business = Business()
			business.business_id = business.formatYellowPagesId(json['id'])
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
					business.geolocation = GeoLocation(lat, lon)
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
			
	def addRequiredParamsToUrl(self, url):
		apiKey = '&apikey=' + self.API_KEY
		clientIP = AppSettingsService().clientIP()
		clientParams = '&UID=' + clientIP
		return url + apiKey + clientParams

class YellowPages_BusinessService:
	def updateBusinessUrl(self, yellowpages_id, url):
		business = Yellowpages_Business()
		business.yellowpages_id = yellowpages_id
		business.url = url
		Yellow_Pages_Business_Repository().save(business)
	
	def getBusinesses(self):
		businesses = Yellow_Pages_Business_Repository().getAllBusinesses()
		for business in businesses:
			logging.info('id: ' + business.yellowpages_id + ' url: ' + business.url)
		return businesses
		
	def getBusinessByYellowPagesId(self, yellowpages_id):
		return Yellow_Pages_Business_Repository().getBusinessByYellowPagesId(yellowpages_id)
		
	def getBusinessesByNameInCity(self, name, city):
		if not name:
			yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByCity(city)
		else:
			yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByNameInCity(name, city)
		return self.combineBusinesses(yellowpages_businesses)
	
	def getBusinessesByGeoLocation(self, latitude, longitude):
		yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByGeoLocation(latitude, longitude)
		return self.combineBusinesses(yellowpages_businesses)
		
	def getBusinessByDetails(self, yellowpages_id, name, provice):
		yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessByIdWithNameInProvince(yellowpages_id, name, provice)
		return self.combineBusiness(yellowpages_businesses)
		
	def combineBusinesses(self, yellowpages_businesses):
		combined_businesses = []
		for business in yellowpages_businesses:
			combinedBusiness = self.combineBusiness(business)
			combined_businesses.append(combinedBusiness)
		return combined_businesses
		
	def combineBusiness(self, business):
		repo_business = Yellow_Pages_Business_Repository().getBusinessByYellowPagesId(business.business_id)
		if repo_business:
			business.url = repo_business.url
		return business

class BusinessService:
	def saveBusiness(self, business):
		dbBusiness = Business_Model()
		dbBusiness.Name = business.name
		Business_Model_Repository().save(dbBusiness)
	
	def getBusinesses(self):
		dbBusinesses = Business_Model_Repository().getAllBusinesses()
		business = Business()
		business.name = dbBusinesses[0].name
		return business

class JsonService:
	def getJsonForBusinessWithYellowPagesId(self, yellowpages_id):
		business = YellowPages_BusinessService().getBusinessByYellowPagesId(yellowpages_id)
		return BusinessEncoder().encode(business)
		
	def getJsonForBusinessesInCity(self, city):
		businesses = YellowPages_BusinessService().getBusinessesByNameInCity('', city)
		return self.encodeBusinesses(businesses)
		
	def getJsonForBusinessesInGeoLocation(self, latitude, longitude):
		businesses = YellowPages_BusinessService().getBusinessesByGeoLocation(latitude, longitude)
		return self.encodeBusinesses(businesses)
	
	def getJsonForBusinessWithDetails(self, yellowpages_id, province, name):
		business = YellowPages_BusinessService().getBusinessByDetails(yellowpages_id, name, province)
		return BusinessEncoder().encode(business)
	
	def encodeBusinesses(self, businesses):
		jsonData = []
		for business in businesses:
			encodedBusiness = BusinessEncoder().encode(business)
			jsonData.append(json.loads(encodedBusiness))
		jsonBusinesses = JsonListEncoder().encode(jsonData)
		return '{ "items": ' + jsonBusinesses + '}'
		
class BusinessEncoder(json.JSONEncoder):
	# json serialization example: http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
	def default(self, business):
		if not isinstance (business, Business):
			print 'You cannot use the JSON custom MyClassEncoder for a non-MyClass object.'
			return
		geolocationString = None
		if business.geolocation:
			geolocationString = {'latitude': business.geolocation.latitude, 'longitude': business.geolocation.longitude }
		return {'url': business.url, 'yellowpages_id': business.business_id, 'name': business.name, 'address': 
		{'province': business.province, 'country': business.country, 'city': business.city, 'street': business.street}, 
		'phoneNumber': business.phonenumber, 'geoCode': geolocationString, 'business_id': business.business_id }
		
class JsonListEncoder(json.JSONEncoder):
	def default(self, o):
		try:
			iterable = iter(o)
		except TypeError:
			pass
		else:
			return list(iterable)
		return JSONEncoder.default(self, o)