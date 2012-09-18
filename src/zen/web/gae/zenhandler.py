

class ZenHandler(object):
    def __init__(self,handler=None):
        if handler:
            self.handler=handler

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self,value):
        self._handler=value
        self.request=value.request
        self.response=value.response


    def get(self,param,default_value=""):
        values=self.request.get_all(param)
        if not values: return default_value
        if len(values)==1: return values[0]
        return values

    def redirect(self,uri):
        return self.handler.redirect(uri)

    def write(self,content):
        return self.response.write(content)







