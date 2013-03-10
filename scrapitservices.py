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
from services import YellowPages_BusinessService

#get geo coordinates by address
#108 20103rd st, saskatoon, sk
#http://maps.googleapis.com/maps/api/geocode/json?address=108%20103rd%20St%20E%2C%20Saskatoon%2C%20SK&sensor=true&region=ca

class CreateBusiness(webapp.RequestHandler):
    def get(self):
        businesses = Yellow_Pages_Business_Repository().getAllBusinesses();
        
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

        path = os.path.join(os.path.dirname(__file__), 'test.html')
        self.response.out.write(template.render(path, template_values))

class BusinessHandler(webapp.RequestHandler):
  def post(self):
    business = Yellowpages_Business()

    business.name = self.request.get('name')
    business.yellowpages_id = self.request.get('yellowpages_id')
    business.url = self.request.get('url')
    Yellow_Pages_Business_Repository().save(business)
    self.redirect('/scrapitservices/')

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
        
        self.redirect('/scrapitservices/yellowpagesbussearch')

application = webapp.WSGIApplication([
  ('/scrapitservices/', CreateBusiness),
  ('/scrapitservices/business', BusinessHandler),
  ('/scrapitservices/yellowpagesbussearch', YellowpagesBusinessSearchHandler),
  ('/scrapitservices/addbusinessdetails', AddBusinessDetailsHandler)
  
], debug=AppSettingsService().appInDebugMode())


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()