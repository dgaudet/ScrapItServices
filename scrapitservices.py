import webapp2
import cgi
import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users
from appsettings import AppSettingsService
from services import YellowPages_BusinessService

class YellowpagesBusinessSearch(webapp2.RequestHandler):
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

        path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinessess.html')
        self.response.out.write(template.render(path, template_values))

    
    def post(self):
      logging.info('***YellowpagesBusinessSearchHandler post')
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
      path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinessess.html')
      self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/scrapitservices/', YellowpagesBusinessSearch),
  ('/scrapitservices/update', YellowpagesBusinessSearch)
  
], debug=AppSettingsService().appInDebugMode())