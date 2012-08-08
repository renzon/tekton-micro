'''
Created on 12/07/2011

@author: Renzo Nuccitelli
'''
import unittest
from zen.dataprocess import validation


class ValidationTests(unittest.TestCase):
    def testBooleanValidator(self):
        self.assertEquals(None,validation.boolean_validator(None))
        self.assertEquals(None,validation.boolean_validator("true"))
        self.assertEquals(None,validation.boolean_validator("false"))
        self.assertEquals(None,validation.boolean_validator("True"))
        self.assertEquals(None,validation.boolean_validator("False"))
        self.assertEquals(validation.BR_ERROR_MSGS[validation.INVALID_BOOLEAN]\
                          ,validation.boolean_validator("tru"))
        
        
    def testComposition(self):
        f=validation.composition(validation.required_str,lambda value: value=="foo" and "fooError" or None)
        self.assertEquals(validation.BR_ERROR_MSGS[validation.REQUIRED_MSG], f(""))
        self.assertEquals(validation.BR_ERROR_MSGS[validation.REQUIRED_MSG], f(None))
        self.assertEquals("fooError", f("foo"))
        self.assertTrue(f("Bazz") is None)
                
    def testBrPhone(self):
        lf=validation.br_phone    
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_PHONE], lf("(12) 3456-789"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_PHONE], lf("(12) 3456-78901"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_PHONE], lf("(12) 3456-789A"))
        self.assertEqual(None, lf("(12) 3456-7890"))
        self.assertEqual(None, lf("1234567890"))
        
    def testCEP(self):
        lf=validation.cep    
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_CEP], lf("3456-789"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_CEP], lf("993456-789"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_CEP], lf("83456-7890"))
        self.assertEqual(None, lf("44456-789"))
        self.assertEqual(None, lf("12345678"))
        
    def test_br_currency(self):
        lf=validation.brcurrency    
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_INT], lf("A"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_INT], lf("R$ "))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_INT], lf("83456-7890"))
        self.assertEqual(None, lf("1.000.000,00"))
        self.assertEqual(None, lf("R$ 1.234.567,89"))
        
    def test_brdate(self):
        lf=validation.brdate    
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_BR_DATE], lf("13/13/1982"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_BR_DATE], lf("32/12/1982"))
        self.assertEqual(validation.BR_ERROR_MSGS[validation.INVALID_BR_DATE], lf("2/3/4"))
        self.assertEqual(None, lf("02/09/1982"))
        self.assertEqual(None, lf("31/12/1982"))
        