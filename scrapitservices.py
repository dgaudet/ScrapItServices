import webapp2
import cgi
import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users
from appsettings import AppSettingsService
from services import YellowPages_BusinessService

# can I redirect with the original search params, call the handler directly, or just redirict to scrapitservices/?name=&city=
# need the name and city used to perform the search, when posting the update or hide

class YellowpagesBusinessSearch(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': users.get_current_user(),
			'url_linktext': url_linktext,
		}

		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinessess.html')
		self.response.out.write(template.render(path, template_values))

	def post(self):
		name = cgi.escape(self.request.get('name'))
		city = cgi.escape(self.request.get('city'))
		businesses = YellowPages_BusinessService().getBusinessesByNameInCity(name, city)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': users.get_current_user(),
			'search_performed': True,
			'businesses': businesses,
			'search_name': name,
			'search_city': city
		}
		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinessess.html')
		self.response.out.write(template.render(path, template_values))
		
class YellowPagesBusinessModalHandler(webapp2.RequestHandler):
	def get(self):
		business = None
		error = None
				
		business_id = cgi.escape(self.request.get('business_id'))
		form_type = cgi.escape(self.request.get('form_type'))

		if business_id:
			business = YellowPages_BusinessService().getBusinessByYellowPagesId(business_id)	
		
		if form_type == 'update':
			form_text = 'Update'
		else:
			form_text = 'Hide'
		
		if not users.get_current_user():
			error = 'Sorry there was a problem loading the business'

		template_values = {
			'error': error,
			'business': business,
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
			YellowPages_BusinessService().updateBusinessUrl(yellowpages_id, url=url, hidden=hidden)
		if form_type == 'hide':
			yellowpages_id = cgi.escape(self.request.get('yellowpages_id'))
			YellowPages_BusinessService().updateBusinessUrl(yellowpages_id, hidden=True)

		name = cgi.escape(self.request.get('name'))
		city = cgi.escape(self.request.get('city'))
		logging.info('---------name: ' + str(name) + ' city ' + str(city))
		businesses = YellowPages_BusinessService().getBusinessesByNameInCity(name, city)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': users.get_current_user(),
			'search_performed': True,
			'businesses': businesses,
			'url': url,
			'url_linktext': url_linktext,
			'search_name': name,
			'search_city': city
		}
		path = os.path.join(os.path.dirname(__file__), 'yellowpagesbusinessess.html')
		self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/scrapitservices/', YellowpagesBusinessSearch),
  ('/scrapitservices/loadModal', YellowPagesBusinessModalHandler),
  ('/scrapitservices/updateModal', YellowPagesBusinessModalHandler)
  
], debug=AppSettingsService().appInDebugMode())