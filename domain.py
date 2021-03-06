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
	name = str
	country = str
	province = str
	city = str
	street = str
	postalcode = str
	geolocation = GeoLocation()
	phonenumber = str
	url = str
	business_id = str
	hidden = bool
	
	def __init__(self):
		self.name = None
		self.country = None
		self.province = None
		self.city = None
		self.street = None
		self.postalcode = None
		self.geolocation = None
		self.phonenumber = None
		self.url = None
		self.business_id = None
		self.hidden = None
		
class Province:
	name = str
	code = str
	
	def __init__(self, name = None, code = None):
		self.name = name
		self.code = code
		
class ApiClient:
	name = str
	key = str
	
	def __init__(self, name = None, key = None):
		self.name = name
		self.key = key