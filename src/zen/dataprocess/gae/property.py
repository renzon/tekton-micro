from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadValueError
import hashlib
import random
from zen.dataprocess import validation, transform
from webapp2_extras import security

class BaseStringProperty(ndb.StringProperty):
    def transformation(self,value):
        return value
  
    def validation(self,value):
        raise NotImplemented("Must be implemented")
    def _validate(self, value):
        error=self.validation(value)
        if error:
            raise BadValueError((error+' :%s') % str(value))
        return self.transformation(value)

class BaseIntegerProperty(ndb.IntegerProperty):
    def transformation(self,value):
        return value
  
    def validation(self,value):
        raise NotImplemented("Must be implemented")
    
    def _validate(self, value):
        error=self.validation(value)
        if error:
            raise BadValueError((error+' :%s') % str(value))
        return self.transformation(value)
    

class CEPProperty(BaseStringProperty):
    def validation(self, value):
        return validation.cep(value)

    def transformation(self,value):
        return transform.cep(value)


class BrPhoneProperty(BaseStringProperty):
    def validation(self, value):
        return validation.br_phone(value)

    def transformation(self,value):
        return transform.brphone(value)


class BrCurrencyProperty(BaseIntegerProperty):
    def validation(self, value):
        return validation.brcurrency(value)

    def transformation(self,value):
        return transform.brcurrency(value)



class Password(object):
    def __init__(self,hs=None, pw=None,pepper=None):
        if hs is None and  pw is None:
            self.hs=None
        elif hs:
            self.hs=hs
        else:
            self.hs=security.generate_password_hash(pw,pepper=pepper)
            
    def __eq__(self,y):
        return self.hs==y.hs
            
    def __hash__(self, *args, **kwargs):
        return hash(self.hs)

    
    def check(self, pw,pepper=None):
        return security.check_password_hash(pw, self.hs, pepper)
      
    
    
        


class PasswordProperty(ndb.StringProperty):
    def _to_base_type(self, password):
        return password.hs

    def _from_base_type(self, hs):
        return Password(hs)


