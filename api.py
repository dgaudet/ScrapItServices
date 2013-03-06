import cgi
import wsgiref.handlers
import logging

from services import JsonService
from appsettings import AppSettingsService
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class businessById(webapp.RequestHandler):
	def get(self, yellowpages_id):
		json = JsonService().getJsonForBusinessWithYellowPagesId(yellowpages_id)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)
        
class BusinessByCity(webapp.RequestHandler):
	def get(self, city):
		json = JsonService().getJsonForBusinessesInCity(city)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByLocation(webapp.RequestHandler):
	def get(self):
		latitude = cgi.escape(self.request.get('latitude'))
		longitude = cgi.escape(self.request.get('longitude'))
		json = JsonService().getJsonForBusinessesInGeoLocation(latitude, longitude)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByDetails(webapp.RequestHandler):
	def get(self):
		yellowpages_id = cgi.escape(self.request.get('id'))
		province = cgi.escape(self.request.get('province'))
		name = cgi.escape(self.request.get('name'))
		json = JsonService().getJsonForBusinessWithDetails(yellowpages_id, province, name)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

application = webapp.WSGIApplication([
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


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()