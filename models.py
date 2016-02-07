from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty(required = True)
    age = ndb.IntegerProperty()
    likes = ndb.StringProperty(repeated=True)
    # image = ndb.BlobProperty()
    image_link = ndb.StringProperty()
    bio = ndb.TextProperty(indexed = False)
    gender = ndb.StringProperty(required = True)
    zipcode = ndb.StringProperty()

class Activity(ndb.Model):
    name = ndb.StringProperty(required=True)
    user = ndb.KeyProperty(repeated = True)

#
# class Group(ndb.Model):
#
