from domain import domain
from google.appengine.ext import db

class Yellowpages_Business_Repository:
    def save(business):
        business.put();