import logging
from google.appengine.ext import db

class Business_Repository:
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
        return db.GqlQuery("SELECT * FROM Business");
        
    def getBusinessByYellowPagesId(self, yellowpages_id):        
        query = db.GqlQuery("SELECT * FROM Business where yellowpages_id = :1", yellowpages_id)
        business = query.get()
        if business:
            logging.info('bus 1 id: ' + business.yellowpages_id + ' url: ' + business.url)            
        else:
            logging.info('id: ' + yellowpages_id + ' not found')
        return business