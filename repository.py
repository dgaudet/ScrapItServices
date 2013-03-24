import logging
from google.appengine.ext import db

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
            existingBusiness.put()
            logging.info('********************* updating entity with name: ' + business.name)
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
            logging.info('bus 1 name: ' + business.name + ' url: ' + business.url)            
        else:
            logging.info('busness with name: ' + name + ' not found')
        return business

class Business_Model(db.Model):
	name = db.StringProperty(multiline=False)
	country = db.StringProperty(multiline=False)
	province = db.StringProperty(multiline=False)
	city = db.StringProperty(multiline=False)
	street = db.StringProperty(multiline=False)
	postalcode = db.StringProperty(multiline=False)
	geolocation = db.GeoPtProperty()
	phonenumber = db.StringProperty(multiline=False)
	url = db.StringProperty(multiline=False)
	created_date = db.DateTimeProperty(auto_now_add=True)