import json, urllib
from domain import Business

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
            if 'geocode' in listing:
                geolocation = listing['geocode']
                lat = geolocation['latitude']
                lon = geolocation['longitude']
            business.url = 'fake url'
            businesses.append(business)
        return businesses
            