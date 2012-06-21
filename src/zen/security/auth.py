'''
Created on 11/06/2012

@author: Renzo Nuccitelli
'''
import hashlib


def authenticate(cookie_str,key):
  if cookie_str:
    try:
      vals=cookie_str.split(",")
      dare=vals[-1].split("=")[-1]
      content=",".join(vals[:-1])
      if dare==sign(content,key):
        return True
    except: pass



def sign(value,key):
  return hashlib.sha1(key+value).hexdigest()


def token(values,key):
  values=[k+"="+v for k,v in values]
  s=",".join(values)
  hash=sign(s,key)
  return s+",h="+hash


