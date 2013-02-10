import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import logging

from services import JsonService
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
		json = JsonService().getJsonForBusinessesInCity(city)
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByLocation(webapp.RequestHandler):
	def get(self, city):
		json = JsonService().getJsonForBusinessesInGeoLocation(52.1300528023, -106.597655886 )
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

class BusinessByDetails(webapp.RequestHandler):
	def get(self, city):
		json = JsonService().getJsonForBusinessWithDetails("scrapbook-studio", "saskatchewan", "7746716" )
		self.response.headers["Content-Type"] = "application/json;charset=UTF-8"		
		self.response.out.write(json)

application = webapp.WSGIApplication([
  ('/api/business/(.*)', businessById),
  ('/api/businessById/(.*)', businessById),
  ('/api/businessByCity/(.*)', BusinessByCity),
  ('/api/businessByGeoLocation/(.*)', BusinessByCity),
  ('/api/businessByDetails/(.*)', BusinessByCity)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()