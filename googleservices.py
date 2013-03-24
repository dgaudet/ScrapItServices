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
			