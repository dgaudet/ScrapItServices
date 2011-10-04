from google.appengine.ext import db

class Yellowpages_Business(db.Model):
  yellowpages_id = db.StringProperty(multiline=False)
  name = db.StringProperty(multiline=False)
  url = db.StringProperty(multiline=False)

class Business(db.Model):
    name = db.StringProperty(multiline=False)
    country = db.StringProperty(multiline=False)
    province = db.StringProperty(multiline=False)
    city = db.StringProperty(multiline=False)
    street = db.StringProperty(multiline=False)
    geolocation = db.GeoPtProperty()
    phonenumber = db.StringProperty(multiline=False)
    url = db.StringProperty(multiline=False)
    yellowpages_id = db.StringProperty(multiline=False)