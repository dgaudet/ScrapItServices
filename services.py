import json
import urllib
import logging
from domain import Business, GeoLocation
from repository import Yellow_Pages_Business_Repository, Yellowpages_Business, Business_Model_Repository, Business_Model, Province_Repository
from appsettings import AppSettingsService
from googleservices import GoogleGeoCodeService
from google.appengine.ext import db

class ProvinceService:
	__province_repo = Province_Repository()
	def save(self, province):
		self.__province_repo.save(province)
	
	def getAllProvinces(self):
		return self.__province_repo.getAllProvinces()

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
		
	def getBusinessesByFile(self):
		url = '/Users/Dean/Documents/Code/scrapitservices/testJson.json'
		logging.info("called json.load " + url)
		result = json.load(open(url, 'r'))
		return self.buildBusinessFromJson(result)
		
	def getBusinessDetailsByFile(self):
		url = '/Users/Dean/Documents/Code/scrapitservices/onelisting.json'
		logging.info("called json.load " + url)
		result = json.load(open(url, 'r'))
		return self.buildBusinessDetailsFromJson(result)
		
	def getBusinessByIdWithNameInProvince(self, yellowpages_id, name, province):
		#http://api.yellowapi.com/GetBusinessDetails/?prov=Saskatchewan&city=Saskatoon&bus-name=just-scrap-it&listingId=4436892fmt=XML&apikey=a1s2d3f4g5h6j7k8l9k6j5j4&UID=127.0.0.1	
		encodedProvince = urllib.quote(province.encode("utf-8"))
		idWithoutPrefix = self.removePrefixFromId(yellowpages_id)
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
				business.business_id = self.formatYellowPagesId(listing['id'])
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
			business.business_id = self.formatYellowPagesId(json['id'])
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
		
	def formatYellowPagesId(self, id):
		return self.ID_PREFIX + id
		
	def removePrefixFromId(self, id):
		result = id.split(self.ID_PREFIX)
		if len(result) == 2:
			return result[1]
		else:
			return id
			
	def containsPrefix(self, id):
		result = id.split(self.ID_PREFIX)
		if len(result) == 2:
			return True
		else:
			return False

class YellowPages_BusinessService:
	def updateBusinessUrl(self, yellowpages_id, url=None, hidden=None):
		logging.info('-------called with id: ' + yellowpages_id + ' hidden ' + str(hidden))
		business = Yellowpages_Business()
		business.yellowpages_id = yellowpages_id		
		if url != None:
			business.url = url
		if hidden != None:
			business.hidden = hidden
		Yellow_Pages_Business_Repository().save(business)
	
	# deprecated method
	def getBusinesses(self):
		businesses = Yellow_Pages_Business_Repository().getAllBusinesses()
		return businesses
		
	def getBusinessByYellowPagesId(self, yellowpages_id):
		yellowpages_business = YellowpagesBusinessSearchService().getBusinessDetailsByFile()
		return self.combineBusiness(yellowpages_business)
		
	def getBusinessesByNameInCity(self, name, city):
		# yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByFile()
		if not name:
			yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByCity(city)
		else:
			yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByNameInCity(name, city)
		return self.combineBusinesses(yellowpages_businesses)
	
	def getBusinessesByGeoLocation(self, latitude, longitude):
		# yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByFile()
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
			if repo_business.hidden != None:
				business.hidden = repo_business.hidden
		return business

class BusinessService:
	DEFAULT_COUNTRY_CODE = 'CA'
	
	def saveBusiness(self, business):
		business.country = self.DEFAULT_COUNTRY_CODE
		business.geolocation = GoogleGeoCodeService().getGeoLocationByAddress(business)
		
		dbBusiness = self.convertBusinessToDbBusiness(business)
		if dbBusiness:		
			Business_Model_Repository().save(dbBusiness)
	
	def updateBusiness(self, business):
		business.country = self.DEFAULT_COUNTRY_CODE
		business.geolocation = GoogleGeoCodeService().getGeoLocationByAddress(business)
		
		dbBusiness = self.convertBusinessToDbBusiness(business)
		if dbBusiness:
			Business_Model_Repository().updateBusiness(long(business.business_id), dbBusiness)
	
	def getBusinesses(self):
		dbBusinesses = Business_Model_Repository().getAllBusinesses()
		businesses = []
		for dbBusiness in dbBusinesses:
			businesses.append(self.convertDbBusinessToBusiness(dbBusiness))
		return businesses
		
	def getBusinessesByGeolocation(self, geoLocation):
		max_distance = 50000 # in meters 80 km ~ 50 mi
		dbBusinesses = Business_Model_Repository().getBusinessByLatLon(geoLocation.latitude, geoLocation.longitude, max_distance)
		businesses = []
		for dbBusiness in dbBusinesses:
			businesses.append(self.convertDbBusinessToBusiness(dbBusiness))
		return businesses
		
	def getBusinessById(self, business_id):
		dbBusiness = Business_Model_Repository().getBusinessById(long(business_id))
		return self.convertDbBusinessToBusiness(dbBusiness)
			
	def convertGeoLocationToGeoPT(self, geolocation):
		if geolocation:
			return "%.10f,%.10f" % (geolocation.latitude, geolocation.longitude)
		return None
	
	def convertGeoPTToGeoLocation(self, geoPt):
		if geoPt:
			return GeoLocation(geoPt.lat, geoPt.lon)
		return None
		
	def convertBusinessToDbBusiness(self, business):
		dbBusiness = None
		if business:
			dbBusiness = Business_Model()
			dbBusiness.name = business.name
			dbBusiness.url = business.url
			dbBusiness.country = business.country
			dbBusiness.province = business.province
			dbBusiness.city = business.city
			dbBusiness.postalcode = business.postalcode
			dbBusiness.street = business.street
			dbBusiness.phonenumber = business.phonenumber
			if business.geolocation:
				dbBusiness.location = self.convertGeoLocationToGeoPT(business.geolocation)
		return dbBusiness
			
	def convertDbBusinessToBusiness(self, dbBusiness):
		business = None
		if dbBusiness:
			business = Business()
			business.name = dbBusiness.name
			business.url = dbBusiness.url
			business.country = dbBusiness.country
			business.province = dbBusiness.province
			business.city = dbBusiness.city
			business.street = dbBusiness.street
			business.postalcode = dbBusiness.postalcode
			business.phonenumber = dbBusiness.phonenumber
			business.geolocation = self.convertGeoPTToGeoLocation(dbBusiness.location)
			business.business_id = str(dbBusiness.key().id())
		return business

class BusinessFacade:
	def getBusinessesByGeoLocation(self, latitude, longitude):
		businesses = []
		yellowBusinesses = YellowPages_BusinessService().getBusinessesByGeoLocation(latitude, longitude)
		yellowBusinesses = self.businessesWithHiddenRemoved(yellowBusinesses)
		if yellowBusinesses:
			businesses.extend(yellowBusinesses)
			
		manualBusinesses = BusinessService().getBusinessesByGeolocation(GeoLocation(latitude, longitude))
		if manualBusinesses:
			businesses.extend(manualBusinesses)
		return businesses
	
	def getBusinessByDetails(self, business_id, province, name):
		business = None
		if YellowpagesBusinessSearchService().containsPrefix(business_id):
			business = YellowPages_BusinessService().getBusinessByDetails(business_id, name, province)
		else:
			business = BusinessService().getBusinessById(business_id)
		return business
		
	def businessesWithHiddenRemoved(self, businesses):
		visibileBusinesses = []
		for business in businesses:
			if business.hidden == None or business.hidden == False:
				visibileBusinesses.append(business)
		return visibileBusinesses

class JsonService:
	# deprecated method
	def getJsonForBusinessWithYellowPagesId(self, yellowpages_id):
		business = YellowPages_BusinessService().getBusinessByYellowPagesId(yellowpages_id)
		return BusinessEncoder().encode(business)
	
	# deprecated method
	def getJsonForBusinessesInCity(self, city):
		businesses = YellowPages_BusinessService().getBusinessesByNameInCity('', city)
		return self.encodeBusinesses(businesses)
		
	def getJsonForBusinessesByGeoLocation(self, latitude, longitude):
		businesses = BusinessFacade().getBusinessesByGeoLocation(latitude, longitude)
		return self.encodeBusinesses(businesses)
	
	def getJsonForBusinessWithDetails(self, business_id, province, name):
		business = BusinessFacade().getBusinessByDetails(business_id, name, province)
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