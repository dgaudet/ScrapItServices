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

#add a way to create a business probably a new page is needed
# need to figure out how this class works exaclty to add new businesses
#get geo coordinates by address
#108 20103rd st, saskatoon, sk
#http://maps.googleapis.com/maps/api/geocode/json?address=108%20103rd%20St%20E%2C%20Saskatoon%2C%20SK&sensor=true&region=ca

class CreateBusiness(webapp.RequestHandler):
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

        path = os.path.join(os.path.dirname(__file__), 'createbusiness.html')
        self.response.out.write(template.render(path, template_values))

class BusinessHandler(webapp.RequestHandler):
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
  ('/businessservice/', CreateBusiness),
  ('/businessservice/business', BusinessHandler)
  
], debug=AppSettingsService().appInDebugMode())


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()