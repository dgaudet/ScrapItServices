from google.appengine.ext import db

class Yellowpages_Business(db.Model):
  yellowpages_id = db.StringProperty(multiline=False)
  name = db.StringProperty(multiline=False)
  url = db.StringProperty(multiline=False)
