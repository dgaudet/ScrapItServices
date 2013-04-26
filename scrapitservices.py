import webapp2
import cgi
import os
import logging
import urllib

from google.appengine.ext.webapp import template
from google.appengine.api import users
from appsettings import AppSettingsService
from services import YellowPages_BusinessService
from domain import GeoLocation

# can I redirect with the original search params, call the handler directly, or just redirict to scrapitservices/?name=&city=
# need the name and city used to perform the search, when posting the update or hide

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
	loadmodalurl = str
	
	def __init__(self, business = None):
		if business:
			self.name = business.name
			self.country = business.country
			self.province = business.province
			self.city = business.city
			self.street = business.street
			self.postalcode = business.postalcode
			self.geolocation = business.geolocation
			self.phonenumber = business.phonenumber
			self.url = business.url
			self.hidden = business.hidden
			self.business_id = business.business_id
			self.loadmodalurl = self._ModalUrl(business.business_id, business.name, business.province)
			
	def _ModalUrl(self, business_id, name, province):
		url = 'business_id=%s&name=%s&province=%s' % (urllib.quote(business_id.encode("utf-8")), urllib.quote(name.encode("utf-8")), urllib.quote(province.encode("utf-8")))
		return url

class UserService:
	def isUserLoggedIn(self):
		if users.get_current_user():
			return True
		else:
			return False
			
	def teplateData(self, request):
		if self.isUserLoggedIn():
			url = users.create_logout_url(request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(request.uri)
			url_linktext = 'Login'
			
		return { 'user': users.get_current_user(),
		'url_linktext': url_linktext,
		'url': url }

class YellowpagesBusinessSearch(webapp2.RequestHandler):
	def get(self):
		template_values = UserService().teplateData(self.request)

		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinesses.html')
		self.response.out.write(template.render(path, template_values))

	def post(self):
		name = cgi.escape(self.request.get('name'))
		city = cgi.escape(self.request.get('city'))
		businesses = YellowPages_BusinessService().getBusinessesByNameInCity(name, city)
		businessViewModels = []
		for business in businesses:
			viewModel = BusinessViewModel(business)
			businessViewModels.append(viewModel)

		template_values = {
			'search_performed': True,
			'businesses': businessViewModels,
			'search_name': name,
			'search_city': city
		}
		template_values.update(UserService().teplateData(self.request))
		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinesses.html')
		self.response.out.write(template.render(path, template_values))
		
class YellowPagesBusinessModalHandler(webapp2.RequestHandler):
	def get(self):
		business = None
		error = None
				
		business_id = cgi.escape(self.request.get('business_id'))
		name = cgi.escape(self.request.get('name'))
		province = cgi.escape(self.request.get('province'))
		form_type = cgi.escape(self.request.get('form_type'))

		if business_id:
			business = YellowPages_BusinessService().getBusinessByDetails(business_id, name, province)
			if 'yellowpages' in business.url:
				business.url = None
			logging.info('businesses returned ' + business.business_id)
		
		if form_type == 'update':
			form_text = 'Update'
		else:
			form_text = 'Hide'
		
		if not UserService().isUserLoggedIn():
			error = 'Sorry there was a problem loading the business'

		template_values = {
			'error': error,
			'business': business,
			'business_id': business_id,
			'form_type': form_type,
			'form_text': form_text
		}
		
		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinessmodal.html')
		self.response.out.write(template.render(path, template_values))
	
	def post(self):
		form_type = cgi.escape(self.request.get('post_type'))
		if form_type == 'update':
			yellowpages_id = cgi.escape(self.request.get('yellowpages_id'))
			url = cgi.escape(self.request.get('url'))
			hide = cgi.escape(self.request.get('hide'))
			hidden = False
			if hide == 'True':
				hidden = True
			if url == "":
				url = None
			YellowPages_BusinessService().updateBusiness(yellowpages_id, url=url, hidden=hidden)
		if form_type == 'hide':
			yellowpages_id = cgi.escape(self.request.get('yellowpages_id'))
			YellowPages_BusinessService().updateBusiness(yellowpages_id, hidden=True)

		name = cgi.escape(self.request.get('name'))
		city = cgi.escape(self.request.get('city'))
		businesses = YellowPages_BusinessService().getBusinessesByNameInCity(name, city)

		template_values = {
			'search_performed': True,
			'businesses': businesses,
			'search_name': name,
			'search_city': city
		}
		template_values.update(UserService().teplateData(self.request))
		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinesses.html')
		self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/scrapitservices/', YellowpagesBusinessSearch),
  ('/scrapitservices/loadModal', YellowPagesBusinessModalHandler),
  ('/scrapitservices/updateModal', YellowPagesBusinessModalHandler)
  
], debug=AppSettingsService().appInDebugMode())