import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import logging

from domain import Yellowpages_Business
from repository import Business_Repository
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from services import BusinessService

class MainPage(webapp.RequestHandler):
    def get(self):
        businesses = Business_Repository().getAllBusinesses();
        
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
    Business_Repository().save(business)
    self.redirect('/')

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

        path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinesssearch.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        form_type = cgi.escape(self.request.get('post_type'))
        if form_type == 'add':
            yellowpages_id = cgi.escape(self.request.get('yellowpages_id'))
            url = cgi.escape(self.request.get('url'))
            BusinessService().updateBusinessUrl(yellowpages_id, url)
        name = cgi.escape(self.request.get('name'))
        city = cgi.escape(self.request.get('city'))
        businesses = BusinessService().getBusinessesByNameInCity(name, city)
        
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
            'search_name': name,
            'search_city': city
        }

        path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinesssearch.html')
        self.response.out.write(template.render(path, template_values))

class AddBusinessDetailsHandler(webapp.RequestHandler):
    def post(self):
        name = cgi.escape(self.request.get('name'))
        city = cgi.escape(self.request.get('city'))
        
        self.redirect('/yellowpagesbussearch')

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/business', BusinessHandler),
  ('/yellowpagesbussearch', YellowpagesBusinessSearchHandler),
  ('/addbusinessdetails', AddBusinessDetailsHandler)
  
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()