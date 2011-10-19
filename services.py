import json, urllib
import logging
from domain import Business
from repository import Business_Repository
from google.appengine.ext import db

BASE_URL = 'http://api.sandbox.yellowapi.com'
API_KEY = '9k5g4bqucenr9ztnh9x693cw'

class YellowpagesBusinessSearchService:
    def getBusinessesByNameInCity(self, name, city):
        # http://api.sandbox.yellowapi.com/FindBusiness/?what=scrapbook%20studio&where=saskatoon&fmt=JSON&pgLen=10&apikey=9k5g4bqucenr9ztnh9x693cw&UID=127.0.0.1
        url = BASE_URL + '/FindBusiness/?what=' + name + '&where=' + city + '&fmt=JSON&pgLen=10&apikey=' + API_KEY + '&UID=127.0.0.1'
        result = json.load(urllib.urlopen(url))
        listings = result['listings']   
        businesses = []
        for listing in listings:
            business = Business()
            business.yellowpages_id = listing['id']
            business.name = listing['name']
            if 'address' in listing:
                address = listing['address']
                business.city = address['city']
                business.province = address['prov']
                business.country = 'Canada'
                business.street = address['street']
            if 'geoCode' in listing:
                geolocation = listing['geoCode']
                lat = geolocation['latitude']
                lon = geolocation['longitude']
                business.geolocation = str(lat) + ', ' + str(lon)
            # business.url = 'http://google.com'
            businesses.append(business)
        return businesses

class BusinessService:
    def updateBusinessUrl(self, yellowpages_id, url):
        business = Business()
        business.yellowpages_id = yellowpages_id
        business.url = url
        Business_Repository().save(business)
    
    def getBusinesses(self):
        businesses = Business_Repository().getAllBusinesses()
        for business in businesses:
            logging.info('id: ' + business.yellowpages_id + ' url: ' + business.url)
        return businesses
        
    def getBusinessByYellowPagesId(self, yellowpages_id):
        return Business_Repository().getBusinessByYellowPagesId(yellowpages_id)
        
    def getBusinessesByNameInCity(self, name, city):
        yellowpages_businesses = YellowpagesBusinessSearchService().getBusinessesByNameInCity(name, city)
        combined_businesses = []
        for business in yellowpages_businesses:
            repo_business = Business_Repository().getBusinessByYellowPagesId(business.yellowpages_id)
            if repo_business:
                business.url = repo_business.url
            combined_businesses.append(business)
        return combined_businesses