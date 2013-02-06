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

application = webapp.WSGIApplication([
  ('/api/business/(.*)', businessById),
  ('/api/businessById/(.*)', businessById),
  ('/api/businessByCity/(.*)', BusinessByCity)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()