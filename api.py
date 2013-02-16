import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import logging

from services import JsonService
from appsettings import AppSettingsService
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class businessById(webapp.RequestHandler):
	def get(self, yellowpages_id):
		json = JsonService().getJsonForBusinessWithYellowPagesId(yellowpages_id)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)
        
class BusinessByCity(webapp.RequestHandler):
	def get(self, city):
		clientIP = self.request.remote_addr
		json = JsonService().getJsonForBusinessesInCity(city, clientIP)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByLocation(webapp.RequestHandler):
	def get(self):
		latitude = cgi.escape(self.request.get('latitude'))
		longitude = cgi.escape(self.request.get('longitude'))
		clientIP = self.request.remote_addr
		json = JsonService().getJsonForBusinessesInGeoLocation(latitude, longitude, clientIP)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByDetails(webapp.RequestHandler):
	def get(self):
		yellowpages_id = cgi.escape(self.request.get('id'))
		province = cgi.escape(self.request.get('province'))
		name = cgi.escape(self.request.get('name'))
		clientIP = self.request.remote_addr
		json = JsonService().getJsonForBusinessWithDetails(yellowpages_id, province, name, clientIP)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

application = webapp.WSGIApplication([
  ('/api/business/(.*)', businessById),
  ('/api/businessById/(.*)', businessById),
  ('/api/businessByCity/(.*)', BusinessByCity),
  ('/api/businessByGeoLocation', BusinessByLocation),
  ('/api/businessByDetails', BusinessByDetails)
], debug=AppSettingsService().appInDebugMode())


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()