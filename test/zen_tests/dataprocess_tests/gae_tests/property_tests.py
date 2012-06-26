'''
Created on 03/04/2012

@author: Renzo Nuccitelli
'''
import unittest
from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadValueError
from zen.dataprocess.validation import BR_ERROR_MSGS
from zen.dataprocess import validation
from zen.dataprocess.gae.form import Form
from zen.dataprocess.gae import property


class CepTests(unittest.TestCase):
    def test_cep(self):
        class C(ndb.Model):
            cep=property.CEPProperty()
        self.assertRaises(BadValueError, C,cep="1234567")
        self.assertRaises(BadValueError, C,cep="12345-67")
        self.assertRaises(BadValueError, C,cep="12345-6789")
        self.assertRaises(BadValueError, C,cep="1234-5678")
        C(cep="12345678")
        c=C(cep="12345-678")
        self.assertEqual("12345678", c.cep)
        f=Form(C)
        error=f.validate({"cep":"12345-67"})
        self.assertEqual({"cep":BR_ERROR_MSGS[validation.INVALID_CEP]}, error)
    
    def test_br_phone(self):
        class C(ndb.Model):
            phone=property.BrPhoneProperty()
        self.assertRaises(BadValueError, C,phone="123456789")
        self.assertRaises(BadValueError, C,phone="12345678901")
        self.assertRaises(BadValueError, C,phone="(12) 345-67890")
        self.assertRaises(BadValueError, C,phone="(12) 34567-890")
        C(phone="1234567890")
        c=C(phone="(12) 3456-7890")
        self.assertEqual("1234567890", c.phone)
        f=Form(C)
        error=f.validate({"phone":"12345-67"})
        self.assertEqual({"phone":BR_ERROR_MSGS[validation.INVALID_PHONE]}, error)
    
    def test_brcurrency(self):
        class C(ndb.Model):
            cost=property.BrCurrencyProperty()
        self.assertRaises(BadValueError, C,cost="1212,a")
        C(cost=123456789)
        C(cost="123456789")
        C(cost="R$ 1.234.567,89")
        c=C(cost="1.234.567,89")
        self.assertEqual(123456789, c.cost)
        f=Form(C)
        error=f.validate({"cost":"1212,a"})
        self.assertEqual({"cost":BR_ERROR_MSGS[validation.INVALID_INT]}, error)
    
    def test_password(self):
        pw=property.Password(pw="password")
        self.assertIsNotNone(pw.hs)
        pw2=property.Password(pw.hs)
        self.assertEqual(pw.hs, pw2.hs)
        
    #    Wrong Pw
        self.assertFalse(pw2.check("passwor"))
        self.assertFalse(pw2.check("passwords"))
        self.assertFalse(pw2.check("otherpw"))
        
#   right Pw
        self.assertTrue(pw2.check("password"))
        
    #Wrong Pepper
        pw=property.Password(pw="password",pepper="pepper")
        self.assertFalse(pw.check("password"))
        self.assertFalse(pw.check("password","peppe"))
        self.assertFalse(pw.check("password","pepperr"))
        
    #Right Pepper
        self.assertTrue(pw.check("password","pepper"))
    
#    saving the as property
        class C(ndb.Model):
            pw=property.PasswordProperty()
        C(pw=pw)