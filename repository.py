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
	
# class Business_Repository:
# 	# need to modify getBusinessById to get by the db key
#	# need to add a method to getBusinessByName so that we don't insert duplicates, maybe we can check if the key is null
#     def save(self, business):
#         existingBusiness = self.getBusinessById(business.yellowpages_id)
#         if existingBusiness:
#             existingBusiness.url = business.url
#             existingBusiness.put()
#             logging.info('********************* updating entity with yellow id: ' + business.yellowpages_id)
#         else:
#             business.put()
#             logging.info('********************* new entity with yellow id: ' + business.yellowpages_id)
#         
#     def getAllBusinesses(self):
#         """return all DB_Businesses"""
#         return db.GqlQuery("SELECT * FROM DB_Business");
#         
#     def getBusinessById(self, id):        
#         query = db.GqlQuery("SELECT * FROM DB_Business where id = :1", id)
#         business = query.get()
#         if business:
#             logging.info('bus 1 id: ' + business.name + ' url: ' + business.url)            
#         else:
#             logging.info('id: ' + id + ' not found')
#         return business
		
class DB_Business:
	name = db.StringProperty(multiline=False)
	country = db.StringProperty(multiline=False)
	province = db.StringProperty(multiline=False)
	city = db.StringProperty(multiline=False)
	street = db.StringProperty(multiline=False)
	geolocation = db.GeoPtProperty()
	phonenumber = db.StringProperty(multiline=False)
	url = db.StringProperty(multiline=False)