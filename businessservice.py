import cgi
import wsgiref.handlers
import os
import logging

from appsettings import AppSettingsService
from repository import Yellowpages_Business
from repository import Yellow_Pages_Business_Repository
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from services import YellowPages_BusinessService, BusinessService
from domain import Business

# allow users to enter postal code
# add a dropdown for province selection
# use googleservice to get the proper url instead of hardcoding it into the html page

class BusinessHandler(webapp.RequestHandler):
	def get(self):
		businesses = BusinessService().getBusinesses();

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': users.get_current_user(),
			'businesses': businesses,
			'url': url,
			'url_linktext': url_linktext,	
		}
		
		path = os.path.join(os.path.dirname(__file__), 'businesses.html')
		self.response.out.write(template.render(path, template_values))

class CreateBusiness(webapp.RequestHandler):
	def post(self):
		business = Business()

		business.name = cgi.escape(self.request.get('name'))
		business.url = cgi.escape(self.request.get('url'))
		business.province = cgi.escape(self.request.get('province'))
		business.city = cgi.escape(self.request.get('city'))
		business.street = cgi.escape(self.request.get('street'))
		business.phone = cgi.escape(self.request.get('phone'))
		BusinessService().saveBusiness(business);
		
		self.redirect('/businessservice/')

application = webapp.WSGIApplication([
  ('/businessservice/create', CreateBusiness),
  ('/businessservice/', BusinessHandler)
  
], debug=AppSettingsService().appInDebugMode())


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()