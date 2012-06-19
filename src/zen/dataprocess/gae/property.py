from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadValueError
import hashlib
import random
from zen.dataprocess import validation, transform

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
    _divider="$"
    def __init__(self,hash=None, pw=None):
        if hash is None and  pw is None:
            raise BadValueError("hash and pw can not be none at same time")
        if hash:
            self.hash=hash
            self.salt=hash.split(Password._divider)[0]
        else:
            self.salt=str(random.random())
            hash=hashlib.sha512(self.salt+pw).hexdigest()
            self.hash=self.salt+Password._divider+hash

    
    def check(self, pw):
        hash=hashlib.sha512(self.salt+pw).hexdigest()
        return self.hash==self.salt+Password._divider+hash
      
    
    
        


class PasswordProperty(ndb.StringProperty):
    def _to_base_type(self, password):
        return password.hash

    def _from_base_type(self, hash):
        return Password(hash)


