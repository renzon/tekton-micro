from google.appengine.ext import ndb

__author__ = 'renzo'

class Example(ndb.Model):
    b=ndb.IntegerProperty()
    name=ndb.StringProperty()
    ap=ndb.FloatProperty()


print Example._properties
print Example._kind_map

print Example._values
print dir(Example)
