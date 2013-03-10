import logging
from google.appengine.ext import db

class Business(db.Model):
	YELLOW_PAGES_ID_PREFIX = 'yellowPagesId:'
	
	name = db.StringProperty(multiline=False)
	country = db.StringProperty(multiline=False)
	province = db.StringProperty(multiline=False)
	city = db.StringProperty(multiline=False)
	street = db.StringProperty(multiline=False)
	geolocation = db.GeoPtProperty()
	phonenumber = db.StringProperty(multiline=False)
	url = db.StringProperty(multiline=False)
	yellowpages_id = db.StringProperty(multiline=False)
	
	def formatYellowPagesId(self, id):
		return self.YELLOW_PAGES_ID_PREFIX + id
		
	def removePrefixFromId(self, id):
		result = id.split(self.YELLOW_PAGES_ID_PREFIX)
		if result.count == 2:
			return result[1]
		else:
			return id