import webapp2
import os
import logging

from appsettings import AppSettingsService
from google.appengine.ext.webapp import template
from services import UserService

class MainPage(webapp2.RequestHandler):
	def get(self):            
		template_values = UserService().teplateData(self.request)

		path = os.path.join(os.path.dirname(__file__), 'resume.html')
		self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/about/resume', MainPage)
  
], debug=AppSettingsService().appInDebugMode())