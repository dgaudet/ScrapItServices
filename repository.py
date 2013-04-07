import logging
from domain import Province
from google.appengine.ext import db
from geo.geomodel import GeoModel
from geo import geotypes

class Yellow_Pages_Business_Repository:
    def save(self, business):
        existingBusiness = self.getBusinessByYellowPagesId(business.yellowpages_id)
        if existingBusiness:
            existingBusiness.url = business.url
            existingBusiness.put()
            logging.info('********************* updating entity with yellow id: ' + business.yellowpages_id)
        else:
            business.put()
            logging.info('********************* new entity with yellow id: ' + business.yellowpages_id)
        
    def getAllBusinesses(self):
        """return all Yellowpages_Businesses"""
        return db.GqlQuery("SELECT * FROM Yellowpages_Business");
        
    def getBusinessByYellowPagesId(self, yellowpages_id):        
        query = db.GqlQuery("SELECT * FROM Yellowpages_Business where yellowpages_id = :1", yellowpages_id)
        business = query.get()
        if business:
            logging.info('bus 1 id: ' + business.yellowpages_id + ' url: ' + business.url)            
        else:
            logging.info('id: ' + yellowpages_id + ' not found')
        return business

class Yellowpages_Business(db.Model):
	yellowpages_id = db.StringProperty(multiline=False)
	name = db.StringProperty(multiline=False)
	url = db.StringProperty(multiline=False)

class Business_Model_Repository:
	# doing a put then a getAllBusinesses does not return the data imediately, due to google's high replication data store
	# if I want it too I would need to use strong conistency and ancestor queries https://developers.google.com/appengine/docs/python/datastore/structuring_for_strong_consistency
	# need to modify getBusinessById to get by the db key
	# need to add a method to getBusinessByName so that we don't insert duplicates, maybe we can check if the key is null
	def save(self, business):
		existingBusiness = self.getBusinessByName(business.name)
		if existingBusiness:
			existingBusiness.url = business.url
			existingBusiness.phonenumber = business.phonenumber
			existingBusiness.put()
			logging.info('********************* updating entity with name: ' + business.name + ' phone: ' + business.phonenumber)
		else:
			business.put()
			logging.info('********************* new entity with name: ' + business.name)

	def getAllBusinesses(self):
		"""return all Business_Model"""
		return Business_Model.all().order("name");

	def getBusinessByName(self, name):
		logging.info('name search: ' + name)
		query = Business_Model.gql("WHERE name = :1", name)
		business = query.get()
		if business:
			logging.info('bus 1 name: ' + business.name + ' url: ' + business.url + ' phone: ' + business.phonenumber)            
		else:
			logging.info('busness with name: ' + name + ' not found')
		return business

	def getBusinessById(self, business_id):
		logging.info('id search: ' + str(business_id))
		business = Business_Model.get_by_id(business_id)
		if business:
			logging.info('bus 1 name: ' + business.name + ' url: ' + business.url)            
		else:
			logging.info('busness with id: ' + str(business_id) + ' not found')
		return business
	
	def getBusinessByLatLon(self, latitude, longitude):
		logging.info('lat %s lon %s' % (latitude, longitude))
		max_results = 100
		max_distance = 80000 # 80 km ~ 50 mi
		center = geotypes.Point(latitude, longitude)
		base_query = Business_Model.all()
		base_query.order('name')
		results = Business_Model.proximity_fetch(
		            base_query,
		            center, max_results=max_results, max_distance=max_distance)
		logging.info('results: %s' %', '.join(map(str, results)))
		return results
	
class Business_Model(GeoModel):
	name = db.StringProperty(multiline=False)
	country = db.StringProperty(multiline=False)
	province = db.StringProperty(multiline=False)
	city = db.StringProperty(multiline=False)
	street = db.StringProperty(multiline=False)
	postalcode = db.StringProperty(multiline=False)
	phonenumber = db.StringProperty(multiline=False)
	url = db.StringProperty(multiline=False)
	created_date = db.DateTimeProperty(auto_now_add=True)
	
class Province_Repository:
	__provinces = []
	
	def __init__(self):
		province = Province('Alberta', 'ab')
		self.save(province)
		province = Province('British Columbia', 'bc')
		self.save(province)
		province = Province('Saskatchewan', 'sk')
		self.save(province)
		province = Province('Manitoba', 'mb')
		self.save(province)
		province = Province('Ontario', 'on')
		self.save(province)
		province = Province('Quebec', 'qb')
		self.save(province)
		province = Province('Nova Scotia', 'ns')
		self.save(province)
		province = Province('Northwest Territories', 'nw')
		self.save(province)
	
	def save(self, province):
		self.__provinces.append(province)
	
	def getAllProvinces(self):
		return self.__provinces