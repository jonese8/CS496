from google.appengine.ext import ndb

class myStoredData(ndb.Model):
  userInputKeyName = ndb.StringProperty(required=True)
  userInputValName = ndb.StringProperty(required=True)
  restricted = ndb.BooleanProperty(required=True)
  timestamp = ndb.DateTimeProperty(auto_now_add=True)

class cardObject(ndb.Model):
  created_timmestamp = ndb.DateTimeProperty(auto_now_add=True)
  modified_timestamp = ndb.DateTimeProperty(auto_now=True)
  cardType = ndb.StringProperty(required=True)
  includedIn = ndb.StringProperty(repeated=True)
  cardName = ndb.StringProperty(required=True)
  cardDesc = ndb.TextProperty()
  cardTags = ndb.StringProperty(repeated=True)
  addedBy = ndb.UserProperty()
  modifiedBy = ndb.UserProperty()





