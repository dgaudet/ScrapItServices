import webapp2
import cgi
import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users
from appsettings import AppSettingsService
from services import BusinessService
from domain import Business, GeoLocation
from googleservices import GoogleMapsService

# allow users to enter postal code
# add a dropdown for province selection
# use googleservice to get the proper url instead of hardcoding it into the html page

class BusinessViewModel:
	name = str
	country = str
	province = str
	city = str
	street = str
	postalcode = str
	geolocation = GeoLocation()
	mapurl = str
	phonenumber = str
	url = str
	business_id = str
	
	def __init__(self, business = None):
		if business:
			mapService = GoogleMapsService()
			self.name = business.name
			self.country = business.country
			self.province = business.province
			self.city = business.city
			self.street = business.street
			self.postalcode = business.postalcode
			self.geolocation = business.geolocation
			self.mapurl = mapService.getMapUrlForGeoLocation(business.geolocation)
			self.phonenumber = business.phonenumber
			self.url = business.url
			self.business_id = business.business_id

class BusinessHandler(webapp2.RequestHandler):
	def get(self):
		businesses = BusinessService().getBusinesses();
		businessViewModels = []
		for business in businesses:
			businessViewModel = BusinessViewModel(business)			
			businessViewModels.append(businessViewModel)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': users.get_current_user(),
			'businesses': businessViewModels,
			'url': url,
			'url_linktext': url_linktext,	
		}
		
		path = os.path.join(os.path.dirname(__file__), 'businesses.html')
		self.response.out.write(template.render(path, template_values))

class CreateBusiness(webapp2.RequestHandler):
	def post(self):
		business = Business()

		business.name = cgi.escape(self.request.get('name'))
		business.url = cgi.escape(self.request.get('url'))
		business.province = cgi.escape(self.request.get('province'))
		business.city = cgi.escape(self.request.get('city'))
		business.street = cgi.escape(self.request.get('street'))
		business.phonenumber = cgi.escape(self.request.get('phone'))
		BusinessService().saveBusiness(business);
		
		self.redirect('/businessservice/')
			
app = webapp2.WSGIApplication([
  ('/businessservice/create', CreateBusiness),
  ('/businessservice/', BusinessHandler)
  
], debug=AppSettingsService().appInDebugMode())