import webapp2
import logging

from appsettings import AppSettingsService

class StatusHandler(webapp2.RequestHandler):
	def get(self):
		self.printVariableToPage("App_Engine_Type", AppSettingsService().appEngineType())
		self.printVariableToPage("App_Version", AppSettingsService().appVersion())
		self.printVariableToPage("Server_Name", AppSettingsService().serverName())		
		self.printVariableToPage("Application_ID", AppSettingsService().applicationID())
		self.printVariableToPage("YellowPages_Base_URL", AppSettingsService().yellowPagesBaseUrl())
		self.printVariableToPage("YellowPages_API_Key", AppSettingsService().yellowPagesApiKey())
		self.printVariableToPage("Request_IP", AppSettingsService().clientIP())
		#display the fact that I am using I think jinja2 - whatever the default is for the templating language
		#also using webapp2 for the web application framework
		
	def printVariableToPage(self, variableName, variableValue):
		self.response.out.write("%s = %s<br />\n" % (variableName, variableValue))

app = webapp2.WSGIApplication([
  ('/status', StatusHandler)
  
], debug=AppSettingsService().appInDebugMode())