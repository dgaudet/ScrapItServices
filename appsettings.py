import os

class AppSettingsService:
	def appInDebugMode(self):
		if(self.appEngineType().lower().find('development') == 0):
			return True
		else:
			return False
	
	def appEngineType(self):
		return os.environ['SERVER_SOFTWARE']
	
	def appVersion(self):
		return os.environ['CURRENT_VERSION_ID']
	
	def serverName(self):
		return os.environ['SERVER_NAME']
		
	def clientIP(self):
		return os.environ['REMOTE_ADDR']
		
	def applicationID(self):
		return os.environ['APPLICATION_ID']
		
	def yellowPagesBaseUrl(self):
		if self.appInDebugMode:
			return 'http://api.sandbox.yellowapi.com'
		return 'http://api.yellowapi.com'
		
	def yellowPagesApiKey(self):
		if self.appInDebugMode:
			#Sandbox API key
			return '9k5g4bqucenr9ztnh9x693cw'
		#Production API key
		return 'ycgd3xrz8kxfayety5dpfuzn'