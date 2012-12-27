import datetime
from google.appengine.ext import ndb


__author__ = 'renzo'


def _handle_property_options(fnc):
    def f(property):
        if property._repeated:
            return [fnc(property)]
        elif property._default is not None:
            return property._default
        elif property._choices:
            for c in property._choices:
                return c
        else:
            return fnc(property)
    return f

@_handle_property_options
def _integer_default(property):
    return 1

@_handle_property_options
def _float_default(property):
    return 1.0

@_handle_property_options
def _string_default(property):
    return "default"

#just for dependency injection when testing
_now_fnc=datetime.datetime.now

@_handle_property_options
def _datetime_default(property):
    return _now_fnc()


def _extract_property_base_class(property):
    if isinstance(property,ndb.StringProperty):
        return ndb.StringProperty
    elif isinstance(property,ndb.FloatProperty):
        return ndb.FloatProperty
    elif isinstance(property,ndb.IntegerProperty):
        return ndb.IntegerProperty
    if isinstance(property,ndb.DateTimeProperty):
        return ndb.DateTimeProperty

PROPERTIES_DEFAULT_DICT={
    ndb.IntegerProperty:_integer_default,
    ndb.StringProperty:_string_default,
    ndb.DateTimeProperty:_datetime_default,
    ndb.FloatProperty:_float_default

}

def _generate_default(property):
    property_cls=_extract_property_base_class(property)
    default_fcn=PROPERTIES_DEFAULT_DICT[property_cls]
    return default_fcn(property)


def make_one(cls,**kwargs):
    properties=cls._properties
    generated_kwargs={k:_generate_default(v) for k,v in properties.iteritems()
                    if not k.startswith("_") and not k in kwargs}
    generated_kwargs.update(kwargs)
    return cls(**generated_kwargs)