import datetime
from google.appengine.ext import ndb

#just for dependency injection when testing
_now_fnc=datetime.datetime.now


class PropertyProcessor(object):
    def __init__(self,property_cls):
        self.property_cls=property_cls

    def default(self,property,cls):
        raise NotImplementedError()

    def process(self,property,cls):
        if property._repeated:
            return [self.default(property,cls)]
        elif property._default is not None:
            return property._default
        elif property._choices:
            for c in property._choices:
                return c
        else:
            return self.default(property,cls)


class IntegerProcessor(PropertyProcessor):
    def __init__(self):
        super(IntegerProcessor,self).__init__(ndb.IntegerProperty)

    def default(self,property,cls):
        return 1


class FloatProcessor(PropertyProcessor):
    def __init__(self):
        super(FloatProcessor,self).__init__(ndb.FloatProperty)

    def default(self,property,cls):
        return 1.0


class StringProcessor(PropertyProcessor):
    def __init__(self,property_cls=ndb.StringProperty):
        super(StringProcessor,self).__init__(property_cls)

    def default(self,property,cls):
        return "default"


#Once TextProperty extends BlobProperty, it is enough for both
class BlobProcessor(StringProcessor):
    def __init__(self):
        super(BlobProcessor,self).__init__(ndb.BlobProperty)


class BooleanProcessor(PropertyProcessor):
    def __init__(self):
        super(BooleanProcessor,self).__init__(ndb.BooleanProperty)

    def default(self,property,cls):
        return False


class DatetimeProcessor(PropertyProcessor):
    def __init__(self):
        super(DatetimeProcessor,self).__init__(ndb.DateTimeProperty)

    def default(self,property,cls):
        return _now_fnc()


class DateProcessor(PropertyProcessor):
    def __init__(self):
        super(DateProcessor,self).__init__(ndb.DateProperty)

    def default(self,property,cls):
        return datetime.date.today()


class TimeProcessor(PropertyProcessor):
    def __init__(self):
        super(TimeProcessor,self).__init__(ndb.TimeProperty)

    def default(self,property,cls):
        return _now_fnc().time()


class KeyProcessor(PropertyProcessor):
    def __init__(self):
        super(KeyProcessor,self).__init__(ndb.KeyProperty)

    def default(self,property,cls):
        if property._kind:
            return ndb.Key(property._kind,1)
        return ndb.Key(cls,1)


class GeoProcessor(PropertyProcessor):
    def __init__(self):
        super(GeoProcessor,self).__init__(ndb.GeoPtProperty)

    def default(self,property,cls):
        return ndb.GeoPt(1,1)


class StructuredProcessor(PropertyProcessor):
    def __init__(self):
        super(StructuredProcessor,self).__init__(ndb.StructuredProperty)

    def default(self,property,cls):
        return make_one(property._modelclass)


class LocalStructuredProcessor(PropertyProcessor):
    def __init__(self):
        super(LocalStructuredProcessor,self).__init__(ndb.LocalStructuredProperty)

    def default(self,property,cls):
        return make_one(property._modelclass)


_processors=[]
def add_processor(processor):
    _processors.append(processor)


#initing properties
add_processor(IntegerProcessor())
add_processor(FloatProcessor())
add_processor(StringProcessor())
add_processor(LocalStructuredProcessor())
add_processor(BlobProcessor())
add_processor(BooleanProcessor())
add_processor(DateProcessor())
add_processor(TimeProcessor())
add_processor(DatetimeProcessor())
add_processor(KeyProcessor())
add_processor(GeoProcessor())
add_processor(StructuredProcessor())


def _generate_default(property,cls):
    for p in _processors:
        if isinstance(property,p.property_cls):
            return p.process(property,cls)
    return None


def assignable(name,property):
    return name!="class" and not isinstance(property,ndb.ComputedProperty)


def make_one(cls,**kwargs):
    properties=cls._properties
    generated_kwargs={k:_generate_default(v,cls) for k,v in properties.iteritems()
                    if assignable(k,v) and not k in kwargs}
    generated_kwargs.update(kwargs)
    return cls(**generated_kwargs)