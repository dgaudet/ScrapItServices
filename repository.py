from domain import Yellowpages_Business
from google.appengine.ext import db

class Yellowpages_Business_Repository:
    def save(self, business):
        business.put();
        
    def getAllBusinesses(self):
        """return all Yellowpages_Businesses"""
        return db.GqlQuery("SELECT * FROM Yellowpages_Business");