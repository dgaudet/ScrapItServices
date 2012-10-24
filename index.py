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
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            
        template_values = {
            'url': url,
            'url_linktext': url_linktext
        }
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/', MainPage)
  
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()