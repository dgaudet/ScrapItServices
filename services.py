import json, urllib
from domain import Yellowpages_Business

BASE_URL = 'http://api.sandbox.yellowapi.com'
API_KEY = '9k5g4bqucenr9ztnh9x693cw'

class YellowpagesBusinessSearchService:
    def getBusinessesByNameInCity(self, name, city):
        url = BASE_URL + '/FindBusiness/?what=barber&where=saskatoon&fmt=JSON&pgLen=10&apikey=' + API_KEY + '&UID=127.0.0.1'
        result = json.load(urllib.urlopen(url))
        listings = result['listings']   
        businesses = []     
        for listing in listings:
            business = Yellowpages_Business()
            business.yellowpages_id = listing['id']
            business.name = listing['name']
            business.url = 'fake url'
            businesses.append(business)
        return businesses
        # http://api.sandbox.yellowapi.com/FindBusiness/?what=scrapbook%20studio&where=saskatoon&fmt=JSON&pgLen=10&apikey=9k5g4bqucenr9ztnh9x693cw&UID=127.0.0.1
            