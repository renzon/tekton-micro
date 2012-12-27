from unittest import TestCase
import datetime
from google.appengine.ext import ndb
from zen.gae import mommy

NOW=datetime.datetime.now()

#mocking mommy now function
mommy._now_fnc=lambda : NOW
INTEGER_DEFAULT=3676

INTEGER_CHOICES=[3,2,1]


class Stub(ndb.Model):
    integer=ndb.IntegerProperty()
    integer_repeated=ndb.IntegerProperty(repeated=True)
    integer_choice=ndb.IntegerProperty(choices=INTEGER_CHOICES)
    integer_default=ndb.IntegerProperty(default=INTEGER_DEFAULT)
    float=ndb.FloatProperty()
    string=ndb.StringProperty()
    dtime=ndb.DateTimeProperty()



class MommyTests(TestCase):
    def test_integer_repeated(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertListEqual([1],stub.integer_repeated)
        #with some value
        stub=mommy.make_one(Stub,integer_repeated=[20,21])
        self.assertListEqual([20,21],stub.integer_repeated)

    def test_integer(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(1,stub.integer)
        #with some value
        stub=mommy.make_one(Stub,integer=20)
        self.assertEqual(20,stub.integer)

    def test_integer_default(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(INTEGER_DEFAULT,stub.integer_default)
        #with some value
        stub=mommy.make_one(Stub,integer_default=90)
        self.assertEqual(90,stub.integer_default)

    def test_integer_with_choices(self):
        #default: if there are choices, choose one of them
        stub=mommy.make_one(Stub)
        self.assertIn(stub.integer_choice,INTEGER_CHOICES)
        #with some value
        stub=mommy.make_one(Stub,integer_choice=INTEGER_CHOICES[1])
        self.assertEqual(INTEGER_CHOICES[1],stub.integer_choice)

    def test_float(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(1.0,stub.float)
        #with some value
        stub=mommy.make_one(Stub,float=2.0)
        self.assertEqual(2.0,stub.float)

    def test_string(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual("default",stub.string)
        #with some value
        stub=mommy.make_one(Stub,string="foo")
        self.assertEqual("foo",stub.string)

    def test_datetime(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(NOW,stub.dtime)
        #with some value
        another_date=datetime.datetime(2012,12,27)
        stub=mommy.make_one(Stub,dtime=another_date)
        self.assertEqual(another_date,stub.dtime)
