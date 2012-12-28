from unittest import TestCase
import datetime
from google.appengine.ext import ndb
from google.appengine.ext.ndb.polymodel import PolyModel
from zen.gae import mommy

NOW=datetime.datetime.now()

#mocking mommy now function
mommy._now_fnc=lambda : NOW

INTEGER_DEFAULT=3676
INTEGER_CHOICES=[3,2,1]

class StubPolymodel(PolyModel):
    a=ndb.IntegerProperty()

class ChildStub(StubPolymodel):
    b=ndb.StringProperty()

class StubRelation(ndb.Model):
    ppt=ndb.IntegerProperty()

    def __eq__(self, other):
        if other is None:
            return False
        return self.ppt==other.ppt


class Stub(ndb.Model):
    integer=ndb.IntegerProperty()
    integer_repeated=ndb.IntegerProperty(repeated=True)
    integer_choice=ndb.IntegerProperty(choices=INTEGER_CHOICES)
    integer_default=ndb.IntegerProperty(default=INTEGER_DEFAULT)
    computed=ndb.ComputedProperty(lambda self: self.integer+1)
    float=ndb.FloatProperty()
    string=ndb.StringProperty()
    dtime=ndb.DateTimeProperty()
    dt=ndb.DateProperty()
    b=ndb.BooleanProperty()
    text=ndb.TextProperty()
    relation=ndb.KeyProperty()
    relation_kind=ndb.KeyProperty(StubRelation)
    relation_str=ndb.KeyProperty(kind="StubRelation")
    geo=ndb.GeoPtProperty()
    blob=ndb.BlobProperty()
    structured=ndb.StructuredProperty(StubRelation)
    local=ndb.LocalStructuredProperty(StubRelation)
    js=ndb.JsonProperty()
    pickle=ndb.PickleProperty()
    time=ndb.TimeProperty()


class MommyTests(TestCase):
    def test_polymodel(self):
        child=mommy.make_one(ChildStub)
        self.assertEqual(1,child.a)
        self.assertEqual("default",child.b)

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

    def test_text(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual("default",stub.text)
        #with some value
        stub=mommy.make_one(Stub,text="foo")
        self.assertEqual("foo",stub.text)

    def test_blob(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual("default",stub.blob)
        #with some value
        stub=mommy.make_one(Stub,blob="foo")
        self.assertEqual("foo",stub.blob)

    def test_boolean(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(False,stub.b)
        #with some value
        stub=mommy.make_one(Stub,b=True)
        self.assertTrue(stub.b)

    def test_time(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(NOW.time(),stub.time)
        #with some value
        another_time=datetime.datetime(2012,12,27,9,9,9).time()
        stub=mommy.make_one(Stub,time=another_time)
        self.assertEqual(another_time,stub.time)

    def test_datetime(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(NOW,stub.dtime)
        #with some value
        another_datetime=datetime.datetime(2012,12,27)
        stub=mommy.make_one(Stub,dtime=another_datetime)
        self.assertEqual(another_datetime,stub.dtime)

    def test_date(self):
        #default
        stub=mommy.make_one(Stub)
        today=datetime.date.today()
        self.assertEqual(today,stub.dt)
        #with some value
        another_date=datetime.date(2012,12,27)
        stub=mommy.make_one(Stub,dt=another_date)
        self.assertEqual(another_date,stub.dt)

    def test_key(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(ndb.Key(Stub,1),stub.relation)
        #with some value
        another_key=ndb.Key(StubRelation,3)
        stub=mommy.make_one(Stub,relation=another_key)
        self.assertEqual(another_key,stub.relation)

    def test_key_kind(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(ndb.Key(StubRelation,1),stub.relation_kind)
        #with some value
        another_key=ndb.Key(StubRelation,3)
        stub=mommy.make_one(Stub,relation_kind=another_key)
        self.assertEqual(another_key,stub.relation_kind)

    def test_key_str(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(ndb.Key(StubRelation,1),stub.relation_str)
        #with some value
        another_key=ndb.Key(StubRelation,3)
        stub=mommy.make_one(Stub,relation_str=another_key)
        self.assertEqual(another_key,stub.relation_str)

    def test_geo(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(ndb.GeoPt(1,1),stub.geo)
        #with some value
        another_geo=ndb.GeoPt(2.0,2.0)
        stub=mommy.make_one(Stub,geo=another_geo)
        self.assertEqual(another_geo,stub.geo)

    def test_structured(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(StubRelation(ppt=1),stub.structured)
        #with some value
        structured=StubRelation(ppt=5)
        stub=mommy.make_one(Stub,structured=structured)
        self.assertEqual(structured,stub.structured)

    def test_local(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual(StubRelation(ppt=1),stub.local)
        #with some value
        local=StubRelation(ppt=5)
        stub=mommy.make_one(Stub,local=local)
        self.assertEqual(local,stub.local)

    def test_json(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual("default",stub.js)
        #with some value
        d={"list":[1],"str":"foo"}
        stub=mommy.make_one(Stub,js=d)
        self.assertDictEqual(d,stub.js)

    def test_pickle(self):
        #default
        stub=mommy.make_one(Stub)
        self.assertEqual("default",stub.pickle)
        #with some value
        d={"list":[1],"str":"foo2"}
        stub=mommy.make_one(Stub,pickle=d)
        self.assertDictEqual(d,stub.pickle)
