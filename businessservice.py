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

		business.name = self.request.get('name')
		business.url = self.request.get('url')
		business.province = self.request.get('province')
		business.city = self.request.get('city')
		business.street = self.request.get('street')
		business.phone = self.request.get('phone')
		BusinessService().saveBusiness(business);
		self.redirect('/businessservice/')

class YellowpagesBusinessSearchHandler(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            'user': users.get_current_user(),
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'yellowpagessearch.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        form_type = cgi.escape(self.request.get('post_type'))
        if form_type == 'add':
            yellowpages_id = cgi.escape(self.request.get('yellowpages_id'))
            url = cgi.escape(self.request.get('url'))
            YellowPages_BusinessService().updateBusinessUrl(yellowpages_id, url)
        name = cgi.escape(self.request.get('name'))
        city = cgi.escape(self.request.get('city'))
        businesses = YellowPages_BusinessService().getBusinessesByNameInCity(name, city)
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            'user': users.get_current_user(),
			'search_perfomred': True,
            'businesses': businesses,
            'url': url,
            'url_linktext': url_linktext,
            'search_name': name,
            'search_city': city
        }

        path = os.path.join(os.path.dirname(__file__), 'yellowpagessearch.html')
        self.response.out.write(template.render(path, template_values))

class AddBusinessDetailsHandler(webapp.RequestHandler):
    def post(self):
        name = cgi.escape(self.request.get('name'))
        city = cgi.escape(self.request.get('city'))
        
        self.redirect('/businessservice/yellowpagesbussearch')

class BusinessSearchHandler(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            'user': users.get_current_user(),
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'yellowpagessearch.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        form_type = cgi.escape(self.request.get('post_type'))
        if form_type == 'add':
            yellowpages_id = cgi.escape(self.request.get('yellowpages_id'))
            url = cgi.escape(self.request.get('url'))
            YellowPages_BusinessService().updateBusinessUrl(yellowpages_id, url)
        name = cgi.escape(self.request.get('name'))
        city = cgi.escape(self.request.get('city'))
        businesses = YellowPages_BusinessService().getBusinessesByNameInCity(name, city)
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            'user': users.get_current_user(),
			'search_perfomred': True,
            'businesses': businesses,
            'url': url,
            'url_linktext': url_linktext,
            'search_name': name,
            'search_city': city
        }

        path = os.path.join(os.path.dirname(__file__), 'businesssearch.html')
        self.response.out.write(template.render(path, template_values))

class AddBusinessHandler(webapp.RequestHandler):
    def post(self):
        name = cgi.escape(self.request.get('name'))
        city = cgi.escape(self.request.get('city'))
        
        self.redirect('/businessservice/businesssearch')

application = webapp.WSGIApplication([
  ('/businessservice/', CreateBusiness),
  ('/businessservice/business', BusinessHandler),
  ('/businessservice/yellowpagesbussearch', YellowpagesBusinessSearchHandler),
  ('/businessservice/addbusinessdetails', AddBusinessDetailsHandler),
  ('/businessservice/addbusiness', AddBusinessHandler),
  ('/businessservice/businesssearch', BusinessSearchHandler)
  
], debug=AppSettingsService().appInDebugMode())


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()