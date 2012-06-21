'''
Created on 11/06/2012

@author: Renzo Nuccitelli
'''
import unittest
from zen.security import auth
KEY="some_key"

class AuthTests(unittest.TestCase):
    def test_authenticate(self):
        self.assertIsNone(auth.authenticate(None,KEY))
        #Right source
        sign=auth.sign("key=abc,email=blah,t=9999999",KEY)
        self.assertIsNotNone(auth.authenticate("key=abc,email=blah,t=9999999,h="+sign,KEY))
        #Wrong source    
        self.assertIsNone(auth.authenticate("key=another,email=blah,t=9999999,h="+sign,KEY))
    
    def test_token(self):
        sign=auth.sign("key=abc,email=blah,t=9999999",KEY)
        token=auth.token([("key","abc"),("email","blah"),("t","9999999")],KEY)
        self.assertEqual("key=abc,email=blah,t=9999999,h="+sign,token)
        sign=auth.sign("key=abc,email=blah,t=9999999,a=another",KEY)
        token=auth.token([("key","abc"),("email","blah"),("t","9999999"),("a","another")],KEY)
        self.assertEqual("key=abc,email=blah,t=9999999,a=another,h="+sign,token)
    