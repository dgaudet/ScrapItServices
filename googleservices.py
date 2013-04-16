import json
import logging
import urllib
from domain import Business, GeoLocation

class GoogleGeoCodeService:
	BASE_URL = "http://maps.googleapis.com/maps/api/geocode/json?"
	
	#get geo coordinates by address
	#108 20103rd st, saskatoon, sk
	#http://maps.googleapis.com/maps/api/geocode/json?address=108%20103rd%20St%20E%2C%20Saskatoon%2C%20SK&sensor=true&region=ca
	
	def getGeoLocationByAddress(self, business):
		# return GeoLocation(52.1673866163,-106.637346115)		
		encodedStreet = urllib.quote(business.street.encode("utf-8"))
		encodedCity = urllib.quote(business.city.encode("utf-8"))
		# encodedPostalCode = urllib.quote(business.postalcode.encode("utf-8"))
		searchQuery = "address=" + encodedStreet + "," + encodedCity + "," + business.province + "&sensor=true&region=" + business.country
		url = self.BASE_URL + searchQuery
		logging.info("called json.load " + url)
		result = json.load(urllib.urlopen(url))
		
		return self.getGeoLocationFromJson(result)
		
	def getGeoLocationFromJson(self, json):
		geolocation = None
		if str(json['status']).lower() != 'ok':
			return None
		if 'results' in json:
			results = json['results']
			if len(results) == 1:
				result = results[0]
				if 'geometry' in result:
					if result['geometry']:
						geometry = result['geometry']
						if 'location' in geometry:
							if geometry['location']:
								location = geometry['location']
								geolocation = GeoLocation(location['lat'], location['lng'])
		
		return geolocation

class GoogleMapsService:
	# https://maps.google.com/maps?q=52.13024309999999,+-106.5980011&hl=en&sll=37.0625,-95.677068&sspn=35.821085,79.013672&t=m&z=16
	def getMapUrlForGeoLocation(self, geolocation):
		if geolocation:
			return "https://maps.google.com/maps?q=" + str(geolocation.latitude) + ",+" + str(geolocation.longitude) + "&hl=en&sll=37.0625,-95.677068&sspn=35.821085,79.013672&t=m&z=16"
		
		return "http://maps.google.com"