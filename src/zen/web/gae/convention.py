from zen import router

__author__ = 'renzo'

'''
Created on 02/02/2011

@author: Renzo Nuccitelli
'''

import webapp2

def _get(handler,param,default_value=""):
    values=handler.request.get_all(param)
    if not values: return default_value
    if len(values)==1: return values[0]
    return values

class Handler(webapp2.RequestHandler):
    def get(self):
        self.make_convention()

    def post(self):
        self.make_convention()

    def put(self):
        self.make_convention()

    def delete(self):
        self.make_convention()

    def make_convention(self):
        kwargs={a:_get(self,a) for a in self.request.arguments()}
        print kwargs
        instance_handler, method, args = router.to_handler(self.request.path,**kwargs)
        instance_handler.handler=self
        method(*args,**kwargs)


app = webapp2.WSGIApplication([("/.*",Handler)], debug = False)


