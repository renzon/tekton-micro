'''
Created on 12/07/2011

@author: Renzo Nuccitelli
'''
import functools
import datetime

def to_none(value):
    if value=="":
        return None
    return value

def not_none_or_empty_str(func):
    def f(value):
        if value is None or value=="":
            return to_none(value)
        return func(value)
    return functools.update_wrapper(f,func)    

@not_none_or_empty_str
def to_boolean(value):
        value=value.upper()
        return value=="TRUE"
    
@not_none_or_empty_str
def to_float(value):
    value=value.replace(".","")
    value=value.replace(",",".")
    try:
        return float(value)
    except:
        return None

@not_none_or_empty_str
def to_int(value):
    try:
        return int(value)
    except:
        return None
@not_none_or_empty_str
def brphone(phone):
    p=""
    for i in range(len(phone)):
        if i!=0 and i!=3 and i!=4 and i!=9:
            p+=phone[i]
        else:
            try:
                int(phone[i])
                p+=phone[i]
            except:
                pass
    return p

@not_none_or_empty_str
def cep(cep):
    p=""
    for i in range(len(cep)):
        if i!=5:
            p+=cep[i]
        else:
            try:
                int(cep[i])
                p+=cep[i]
            except:
                pass
    return p

@not_none_or_empty_str
def to_link(link):
    if link.startswith("http://") or link.startswith("https://"):
        return link
    return "http://"+link

        
def composition(*transforms):
    def f(nextTransform,currentTransform):
        return lambda value: currentTransform(nextTransform(value))
    return reduce(f,transforms,lambda value:value)    

@not_none_or_empty_str
def brcurrency(value):
    value=str(value)
    value=value.replace("R$", "").replace(".","").replace(",","")
    return int(value)

@not_none_or_empty_str
def brdate(value):
    return datetime.datetime.strptime(value,"%d/%m/%Y")