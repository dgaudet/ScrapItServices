import webapp2
import os
import logging

from appsettings import AppSettingsService
from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
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

app = webapp2.WSGIApplication([
  ('/', MainPage)
  
], debug=AppSettingsService().appInDebugMode())