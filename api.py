import webapp2
import cgi
import logging

from services import JsonService, ApiClientService
from appsettings import AppSettingsService

class businessById(webapp2.RequestHandler):
	api_key_str = 'apikey'
	
	#deprecated
	def get(self, yellowpages_id):
		json = JsonService().getJsonForBusinessWithYellowPagesId(yellowpages_id)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)
        
class BusinessByCity(webapp2.RequestHandler):
	def get(self, city):
		json = JsonService().getJsonForBusinessesInCity(city)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByLocation(webapp2.RequestHandler):
	api_key_str = 'apikey'
	
	def get(self):
		latitude = cgi.escape(self.request.get('latitude'))
		longitude = cgi.escape(self.request.get('longitude'))
		key = cgi.escape(self.request.get(self.api_key_str))
		if not ApiClientService().isKeyValid(key):
			self.abort(403)
		json = JsonService().getJsonForBusinessesByGeoLocation(latitude, longitude)		
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByDetails(webapp2.RequestHandler):
	api_key_str = 'apikey'
	
	def get(self):
		business_id = cgi.escape(self.request.get('id'))
		province = cgi.escape(self.request.get('province'))
		name = cgi.escape(self.request.get('name'))
		key = cgi.escape(self.request.get(self.api_key_str))
		if not ApiClientService().isKeyValid(key):
			self.abort(403)
		json = JsonService().getJsonForBusinessWithDetails(business_id, province, name)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

app = webapp2.WSGIApplication([
  ('/api/business/(.*)', businessById),
  ('/api/businessById/(.*)', businessById),
  ('/api/businessByCity/(.*)', BusinessByCity),
  ('/api/businessByGeoLocation', BusinessByLocation),
  ('/api/businessByDetails', BusinessByDetails),
  ('/api/v1/business/(.*)', businessById),
  ('/api/v1/businessById/(.*)', businessById),
  ('/api/v1/businessByCity/(.*)', BusinessByCity),
  ('/api/v1/businessByGeoLocation', BusinessByLocation),
  ('/api/v1/businessByDetails', BusinessByDetails)
], debug=AppSettingsService().appInDebugMode())