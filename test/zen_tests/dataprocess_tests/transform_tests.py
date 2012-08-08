'''
Created on 12/07/2011

@author: Renzo Nuccitelli
'''
import unittest
from zen.dataprocess import transform
import datetime



class TrasnformTests(unittest.TestCase):
    def test_boolean_transform(self):
        self.assertEquals(None,transform.to_boolean(None))
        self.assertEquals(None,transform.to_boolean(""))
        self.assertTrue(transform.to_boolean("true"))
        self.assertTrue(transform.to_boolean("True"))
        self.assertTrue(transform.to_boolean("TrUe"))
        self.assertTrue(transform.to_boolean("TRUE"))
        self.assertFalse(transform.to_boolean("false"))
        self.assertFalse(transform.to_boolean("False"))
        self.assertFalse(transform.to_boolean("FaLse"))
        self.assertFalse(transform.to_boolean("FALSE"))
    
    def test_transform_composition(self):
        f=transform.composition(transform.to_none,lambda value: (value is None) and 1 or 0)
        self.assertEquals(1, f(""))
        self.assertEquals(0, f("foo"))

    def test_br_phone_transform(self):
        t=transform.brphone
        self.assertEqual("123456789", t("(12) 3456-789"))
        self.assertEqual("12345678901", t("(12) 3456-78901"))
        
    def test_cep(self):
        t=transform.cep
        self.assertEqual("3456-789", t("3456-789"))
        self.assertEqual("2345678901", t("23456-78901"))
        self.assertEqual("23456789", t("23456-789"))
        
    def test_brcurrency(self):
        t=transform.brcurrency
        self.assertEqual(123456789, t("1.234.567,89"))
        self.assertEqual(123456789, t("R$ 1.234.567,89"))
        
    def test_brdate(self):
        t=transform.brdate
        date=datetime.datetime(1982,9,2)
        self.assertEqual(date, t("02/09/1982"))
        date=datetime.datetime(1999,12,28)
        self.assertEqual(date, t("28/12/1999"))  