import cgi
import datetime
import urllib
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Yellowpages_Business(db.Model):
  yellowpages_id = db.StringProperty(multiline=False)
  name = db.StringProperty(multiline=False)
  url = db.StringProperty(multiline=False)

class MainPage(webapp.RequestHandler):
    def get(self):
        businesses = db.GqlQuery("SELECT * FROM Yellowpages_Business");
        
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
    business.put()
    self.redirect('/')


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/business', BusinessHandler)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()