# -*- coding: utf-8 -*-
'''
Created on 31/01/2011

@author: Renzo Nuccitelli

main module to allow convetion between URL and Python handlers. 

 The Convention:
 
  Supose a Class handler com.module.Handler containing a method called handle
  
  a URL /com/module/Handler/handle should execute the handle method with no args
  a URL /com/module/Handler/handle/param1 should execute the handle method with param1 as first arg
  a URL /com/module/Handler/handle/param1/param2 should execute the handle method with param1 as first arg and param2 as second
  
   and so on...
  
'''


import urllib
from types import  MethodType, ModuleType
import inspect
import functools

#Config


class CengineConfig(object):
    def __init__(self, position, indicator):
        self.position=position
        self.indicator=indicator


config=CengineConfig(1,"handler")
#Defining exceptions
class CEException(Exception):
    def __str__(self):
        return self.msg


class HandlerNotFound(CEException):
    def __init__(self, msg = "webapp-ce did not found a handler for this request"):
        self.msg = msg
        
    

class URLNotFound(CEException):
    def __init__(self, msg = "webapp-ce did not found a URL for this Handler"):
        self.msg = msg
        
prefix='''
last_import_error: '''
      
def find_attr(obj,att_name,default_name):
    try:
        return getattr(obj,att_name)
    except AttributeError:
        return getattr(obj,default_name)
  
def find(obj,params,default_name):
    try:
        if params:
            att=getattr(obj,params[-1])
            params.pop()
            return att 
    except AttributeError: pass
    return getattr(obj,default_name)

  
#Utilities methods
def to_handler(path):
    """
    Used to allow the convention presented on handle module doc
    Returns a Tuple containing the RequestHandlerClass as first item,
    the method name to be executed on the second item 
    and the parameters as a list on last item
    Raises HandlerNotFound Exception if no handler is found
    """
    decoded_path = urllib.unquote(path)
    path_slices = filter(lambda d: d != "", decoded_path.split("/"))
    path_slices=path_slices or ["home","home","index"]
    path_slices.insert(config.position, config.indicator)
#    else:
#      raise HandlerNotFound("Path %s too short, must be >= then: %s "%decoded_path,config.position)
    params = []
    requestHandler = None
    requestHandlerMethod = None
    last_import_error=""
    while len(path_slices) >= 0 :
        module_name = ".".join(path_slices)
        if not module_name:
            module_name=".".join(["home",config.indicator])
            del params[0]
        try:
            module = __import__(module_name)
        except ImportError as e:
            if len(path_slices):
                last_import_error=str(e)
                params.append(urllib.quote(path_slices.pop()))
        else:
            submodule_names = module_name.split(".")[1:]
            try:
                for sub in submodule_names:
                    module = find_attr(module, sub,"home")
                requestHandler = find(module, params,"home")
                requestHandlerMethod = find(requestHandler, params,"index")
                break
            except AttributeError:
                break
    params.reverse()
    
    if requestHandler == None or requestHandlerMethod == None:
        raise  HandlerNotFound(
            "Handler not found for path: " + decoded_path+\
            prefix+last_import_error)
    return (requestHandler, requestHandlerMethod.__name__, params)
  
def dec(fcn):
    def f(*args):
        url=fcn(*args).replace("/"+config.indicator,"")
        return url or "/" 
    return functools.update_wrapper(f, fcn)

def remove_home_index(string):
    args=string.split("/")
    args=[a for a in args if a!="home" and a!="index"]
    return "/".join(args)


@dec
def to_path(handler,*args):
    """
    Used to be used as the inverse functio from path_to_handler
    Given a handler, returns the url follow the convetion present on handler module doc
    Raises URLNotFound if its impossible to determine the URL
    handler must be a a method class, a class or a module
    """
    params=""
    for a in args:
        params+="/"+str(a)
    if handler != None:
        if isinstance(handler, MethodType):
            return remove_home_index(extract_full_module(handler.im_class) + "/" + handler.__name__)+params
        elif isinstance(handler, ModuleType):
            return remove_home_index("/" + handler.__name__.replace(".", "/"))+params
        elif inspect.isclass(handler):
            return remove_home_index(extract_full_module(handler))+params
        else:
            return remove_home_index(extract_full_module(handler.__class__))+params
    raise URLNotFound("webapp-ce did not foud a URL for handler: " + handler)

