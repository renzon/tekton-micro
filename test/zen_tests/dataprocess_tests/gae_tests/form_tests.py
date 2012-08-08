'''
Created on 13/07/2011

@author: Renzo Nuccitelli
'''
from google.appengine.ext import ndb
import unittest
from zen.dataprocess.gae import form
from zen.dataprocess.gae.property import PasswordProperty, Password
import datetime

class Stub(ndb.Model):
    name=ndb.StringProperty(required=True)
    multiline=ndb.StringProperty()
    choice=ndb.StringProperty(choices=["1","2"])
    bo=ndb.BooleanProperty()
    boreq=ndb.BooleanProperty(required=True)
    i=ndb.IntegerProperty()
    i2=ndb.IntegerProperty(required=True)
    f=ndb.FloatProperty()
    f2=ndb.FloatProperty(required=True)
    pw=PasswordProperty()
    dt=ndb.DateProperty()
    dtime=ndb.DateTimeProperty()
   

f=form.Form(Stub)
print f.html("test")

class FormTests(unittest.TestCase):
    def test_fill(self):
        validRequest={"name":"Foo","choice":"2","bo":"true","boreq":"false"}
        validRequest["i"]="0"
        validRequest["i2"]="13"
        validRequest["f"]="0,0"
        validRequest["f2"]="1.000,00"
        validRequest["m"]="b@b.com"
        validRequest["m2"]="b@b.com"
        
        
        stub=Stub(name="B",boreq=True,i2=1,f2=1.1)
        f.fill(validRequest, stub)
        self.assertEquals("Foo",stub.name)
        self.assertEquals("2",stub.choice)
        self.assertEquals(True,stub.bo)
        self.assertEquals(False,stub.boreq)
        self.assertEquals(0,stub.i)
        self.assertEquals(13,stub.i2)
        self.assertEquals(0.0,stub.f)
        self.assertEquals(1000.00,stub.f2)
    
    def test_request_dict(self):
        validRequest={"name":"Foo","choice":"2","bo":"true","boreq":"false"}
        validRequest["i"]="0"
        validRequest["i2"]="13"
        validRequest["f"]="0,0"
        validRequest["f2"]="1.000,00"
        validRequest["multiline"]="multiline"
        validRequest["pw"]=None
        validRequest["dt"]=None
        validRequest["dtime"]=None
        self.assertEquals(validRequest,f.request_dict(validRequest))    
                  
        
    def test_transform(self):
        validRequest={"name":"Foo","choice":"2","bo":"true","boreq":"false"}
        validRequest["i"]="0"
        validRequest["i2"]="13"
        validRequest["f"]="0,0"
        validRequest["f2"]="1.000,00"
        validRequest["pw"]="abcd"
        validRequest["multiline"]="multiline"
        validRequest["dt"]="31/12/1982"
        validRequest["dtime"]="31/12/1982"
        
        modelDict={"name":"Foo","choice":"2","bo":True,"boreq":False}
        modelDict["i"]=0
        modelDict["i2"]=13
        modelDict["f"]=0.0
        modelDict["f2"]=1000.00
        modelDict["multiline"]="multiline"
        modelDict["dt"]=datetime.datetime(1982,12,31)
        modelDict["dtime"]=datetime.datetime(1982,12,31)
        transformed=f.transform(validRequest)
        p=transformed.pop("pw")
        self.assertTrue(p.check("abcd"))
        self.assertEquals(modelDict,transformed)
    def test_validate(self):
        invalidRequest={"name":"","choice":"3","bo":"ba","boreq":""}
        invalidRequest["i"]="a"
        invalidRequest["i2"]=""
        invalidRequest["f"]="a"
        invalidRequest["f2"]=""
        invalidRequest["m2"]=""
        self.assertEquals(8,len(f.validate(invalidRequest)))
        validRequest={"name":"Foo","choice":"2","bo":"true","boreq":"false"}
        validRequest["i"]="0"
        validRequest["i2"]="13"
        validRequest["f"]="0.0"
        validRequest["f2"]="1.000,00"
        validRequest["m"]="b@b.com"
        validRequest["m2"]="b@b.com"
        
        self.assertEquals({},f.validate(validRequest))
        def validator(request):
            if request.get("m")==request.get("m2"):
                return {}
            return {"m":"Different mails"}
        anotherF=form.Form(Stub,requestValidator=validator)
        self.assertEquals({},anotherF.validate(validRequest))
        validRequest["m"]="differnt@bal.com"
        self.assertEquals({"m":"Different mails"},anotherF.validate(validRequest))
    
    def test_exclusion(self):
        k=f.transformations.get("i2")
        self.assertFalse(k is None)
        f2=form.Form(Stub,("i2",))
        k=f2.transformations.get("i2",None)
        self.assertTrue(k is None)
        
        
    def test_date_transformation(self):
        k=f.transformations["dt"]
        self.assertEquals(k(""),None)
        self.assertEquals(k(None),None)
        self.assertEquals(datetime.datetime(1982,12,31),k("31/12/1982"))
        
    def test_datetime_transformation(self):
        k=f.transformations["dtime"]
        self.assertEquals(k(""),None)
        self.assertEquals(k(None),None)
        self.assertEquals(datetime.datetime(1982,12,31),k("31/12/1982"))     
    
    def test_int_transformation(self):
        k=f.transformations["i2"]
        self.assertEquals(k(""),None)
        self.assertEquals(k(None),None)
        self.assertEquals(666,k("666"))
        self.assertEquals(-23,k("-23"))
        self.assertEquals(0,k("0"))
    
    def test_bool_transformation(self):
        k=f.transformations["bo"]
        self.assertEquals(None,k(""))
        self.assertEquals(None,k(None))
        self.assertTrue(k("True"))
        self.assertFalse(k("False"))
    
    def test_float_transformation(self):    
        k=f.transformations["f2"]
        self.assertEquals(None,k(""))
        self.assertEquals(None,k(None))
        self.assertEquals(666,k("666"))
        self.assertEquals(-23,k("-23"))
        self.assertEquals(0,k("0"))
        self.assertEquals(0.01,k("0,01"))
        self.assertEquals(1000780.01,k("1.000.780,01"))
            
    
    
        
    def test_float_validation(self):    
        k=f.validators["f2"]
        self.assertFalse(k("o6") is None)
        self.assertFalse(k("") is None)
        self.assertFalse(k(None) is None)
        self.assertEquals(None,k("666"))
        self.assertEquals(None,k("-23"))
        self.assertEquals(None,k("0"))
        self.assertEquals(None,k("0,01"))
        self.assertEquals(None,k("1.000.780,01"))
        
        k=f.validators["f"]
        self.assertFalse(k("o6") is None)
        self.assertEquals(None,k(""))
        self.assertEquals(None,k(None))
        self.assertEquals(None,k("666"))
        self.assertEquals(None,k("-23"))
        self.assertEquals(None,k("0"))
        self.assertEquals(None,k("0,01"))
        self.assertEquals(None,k("1.000.780,01"))
    
    
    def test_int_validation(self):
        k=f.validators["i2"]
        self.assertFalse(k("o6") is None)
        self.assertFalse(k("") is None)
        self.assertFalse(k(None) is None)
        self.assertEquals(None,k("666"))
        self.assertEquals(None,k("-23"))
        self.assertEquals(None,k("0"))
        
        k=f.validators["i"]
        self.assertFalse(k("o6") is None)
        self.assertEquals(None,k(""))
        self.assertEquals(None,k(None))
        self.assertEquals(None,k("666"))
        self.assertEquals(None,k("-23"))
        self.assertEquals(None,k("0"))
        
        
    def test_bool_validation(self):
        k=f.validators["bo"]
        self.assertFalse(k("3") is None)
        self.assertEquals(None,k(""))
        self.assertEquals(None,k(None))
        self.assertEquals(None,k("True"))
        self.assertEquals(None,k("False"))
        
        k=f.validators["boreq"]
        self.assertFalse(k("3") is None)
        self.assertFalse(k("") is None)
        self.assertFalse(k(None) is None)
        self.assertEquals(None,k("True"))
        self.assertEquals(None,k("False"))
        
    def test_string_validation(self):
        k=f.validators["name"]
        self.assertEquals(form.REQUIRED_FIELD_ERROR_MSG,k(None))
        self.assertEquals(form.REQUIRED_FIELD_ERROR_MSG,k(""))
        self.assertEquals(None,k("foo"))
        
        k=f.validators["choice"]
        self.assertEquals(form.INVALID_OPTION_MSG,k("3"))
        self.assertEquals(None,k(None))
        self.assertEquals(None,k("1"))
        
        k=f.validators["name"]
        multiline='''sdfsdf
        '''
        self.assertEquals(None,k(multiline))
        
        k=f.validators["multiline"]
        self.assertEquals(None,k(multiline))
    