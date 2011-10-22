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

class MainPage(webapp.RequestHandler):
	def get(self):
		json = JsonService().getJsonForBusinessWithYellowPagesId('2108816')
		template_values = {
			'json': json
		}

		path = os.path.join(os.path.dirname(__file__), 'api.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/api', MainPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()