import webapp2
import cgi
import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users
from appsettings import AppSettingsService
from services import BusinessService, ProvinceService
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
	hidden = bool
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
			self.hidden = business.hidden
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

		provinces = ProvinceService().getAllProvinces()
		template_values = {
			'user': users.get_current_user(),
			'businesses': businessViewModels,
			'url': url,
			'url_linktext': url_linktext,
			'provinces': provinces,
		}
		
		path = os.path.join(os.path.dirname(__file__), 'businesses.html')
		self.response.out.write(template.render(path, template_values))
		
class BusinessModalHandler(webapp2.RequestHandler):
	def get(self):
		business = None
		businessViewModel = None
		error = None
		modal_type = 'create'
		
		business_id = cgi.escape(self.request.get('business_id'))
		
		if business_id:
			business = BusinessService().getBusinessById(business_id);		
			if business:
				businessViewModel = BusinessViewModel(business)
				modal_type = 'update'
			else:
				error = 'Sorry there was a problem loading the business'

		if not users.get_current_user():
			error = 'Sorry there was a problem loading the business'

		provinces = ProvinceService().getAllProvinces()
		template_values = {
			'modal_type': modal_type,
			'error': error,
			'business': businessViewModel,
			'provinces': provinces
		}
		
		path = os.path.join(os.path.dirname(__file__), 'businessModal.html')
		self.response.out.write(template.render(path, template_values))
	
	def post(self):
		postType = cgi.escape(self.request.get('createOrUpdate'))

		business_id = cgi.escape(self.request.get('business_id'))
		if postType == 'hide':
			self.__HideBusiness(business_id)
		else:
			business = Business()

			business.name = cgi.escape(self.request.get('name'))
			business.url = cgi.escape(self.request.get('url'))
			business.province = cgi.escape(self.request.get('province'))
			business.city = cgi.escape(self.request.get('city'))
			business.street = cgi.escape(self.request.get('street'))
			business.phonenumber = cgi.escape(self.request.get('phone'))
			hide = cgi.escape(self.request.get('hide'))
			if hide == 'True':
				business.hidden = True
			else:
				business.hidden = False
		
			if postType == 'update':
				business.business_id = business_id
				BusinessService().updateBusiness(business)
			else:
				BusinessService().saveBusiness(business);
				
		self.redirect('/businessservice/')
		
	def __HideBusiness(self, business_id):
		BusinessService().hideBusiness(business_id)

app = webapp2.WSGIApplication([
  ('/businessservice/createOrUpdate', BusinessModalHandler),
  ('/businessservice/', BusinessHandler),
  ('/businessservice/loadModal', BusinessModalHandler)
  
], debug=AppSettingsService().appInDebugMode())