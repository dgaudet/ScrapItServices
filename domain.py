import logging

class GeoLocation:
	latitude = float
	longitude = float

	def __init__(self, latitude = None, longitude = None):
		if latitude:
			self.latitude = float(latitude)
		else:
			self.latitude = None
		if longitude:
			self.longitude = float(longitude)
		else:
			self.longitude = None

class Business:
	YELLOW_PAGES_ID_PREFIX = 'yellowPagesId:'
	
	name = str
	country = str
	province = str
	city = str
	street = str
	geolocation = GeoLocation()
	phonenumber = str
	url = str
	business_id = str
	
	def __init__(self):
		self.name = None
		self.country = None
		self.province = None
		self.city = None
		self.street = None
		self.geolocation = None
		self.phonenumber = None
		self.url = None
		self.business_id = None
	
	def formatYellowPagesId(self, id):
		return self.YELLOW_PAGES_ID_PREFIX + id
		
	def removePrefixFromId(self, id):
		result = id.split(self.YELLOW_PAGES_ID_PREFIX)
		if len(result) == 2:
			return result[1]
		else:
			return id